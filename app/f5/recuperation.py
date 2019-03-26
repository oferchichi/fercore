from f5.bigip import ManagementRoot
import urllib3
import requests
from prettytable import PrettyTable
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from app.models import Equipement, Application, AppType, Environnement, SystemInformation, Nodes, Pools, VirtualServer
from app import db
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from app.f5.f5 import F5

class Recuperation():

    def __init__(self, ip, login, password):
        self.login = login
        self.password = password
        self.ip = ip
        self.mgmt = ManagementRoot(self.ip, self.login, self.password)

    def affichage(self):
        print("[SIMCA][SYNC]: Process Start")
        list_node = []
        elements_node = {}
        type_application = AppType.query.all()
        environnement_application = Environnement.query.all()
        system_application = SystemInformation.query.all()
        virs = self.mgmt.tm.ltm.virtuals.get_collection()
        print("SIMCA][SYNC]: connect to F5 QPA")
        for vir in virs:
            vs_name = vir.name
            application_type = 42
            environnement_type = 42
            si_application = 42
            print("SIMCA][SYNC]: Name : {}".format(vir.name))
            if 'description' in vir.raw:
                description = vir.description
            else:
                description = ""
            if 'destination' in vir.raw:
                destination = vir.destination.split('/')[2].split(':')[0]
                port_ecoute = vir.destination.split('/')[2].split(':')[1]
            else:
                destination = ""
                port_ecoute = ""
            if 'pool' in vir.sourceAddressTranslation:
                snatpool = vir.sourceAddressTranslation['pool']
            else:
                snatpool = None
            for a in type_application:
                if vir.name.find(a.name) != -1:
                    application_type = a.id
                    pass
            for b in environnement_application:
                if vir.name.find(b.name) != -1:
                    environnement_type = b.id
                    pass
            for c in system_application:
                if vir.name.find(c.name) != -1:
                    si_application = c.id
                    pass
            fqdn = "find it"
            createur = "admin"
            trigram = 42
            existing_one = Application.query.filter_by(nomapp=vs_name).first()
            print("SIMCA][SYNC]: check si l'application est dans la base")
            if existing_one is None:
                print("SIMCA][SYNC]: Creation de l'application")
                app = Application(nomapp=vs_name, status="done", fqdn=fqdn,
                                  description=description, createur=createur,
                                  systeminformation=si_application, trigram=trigram,
                                  apptype=application_type, environnement=environnement_type, avability="1")
                vs = VirtualServer(name=vir.name, fullpath=vir.fullPath,
                                   portService=port_ecoute, description=description,
                                   sourceAddresstranslation=vir.sourceAddressTranslation['type'],
                                   snatPool=snatpool, partition="Common", ipvip=destination,
                                   equipement_id=Equipement.id, app_id=app.id)
                try:
                    db.session.add(app)
                    db.session.add(vs)
                    db.session.commit()
                    print("SIMCA][SYNC]: application cree avec success : {}".format(vs_name))
                except Exception as e:
                    db.session.rollback()
                    print("SIMCA][SYNC]: rollbakc {}".format(str(e)))
                if 'pool' in vir.raw:
                    print("SIMCA][SYNC]: Check pool")
                    pool_name = vir.pool.split('/')[2]
                    pool = self.mgmt.tm.ltm.pools.pool.load(name=pool_name)
                    for member in pool.members_s.get_collection():
                        elements_node["nodename"] = member.name.split(':')[0]
                        elements_node["port"] = member.name.split(':')[1]
                        list_node.append(elements_node)
                        print("SIMCA][SYNC]:Creation nodes")                
                    pl = Pools(name=pool_name, fullpath=pool.fullPath, partition="Common", portService=list_node[0]['port'], vs_id=vs.id)
                    try:
                        db.session.add(pl)
                        db.session.commit()
                    except Exception as e:
                        db.session.rollback()
                    for l in list_node:
                        n = Nodes(name=l['nodename'], ip=member.address, fullname=member.name, partition="Common", pool_id=pl.id)
                        try:
                            db.session.add(n)
                            db.session.commit()
                        except Exception as e:
                            db.session.rollback()
            else:
                if self.mgmt.tm.ltm.virtuals.virtual.exists(name=existing_one.nomapp):
                    print("SIMCA][SYNC]: check if virtual existes")
                    pass
                else:
                    print("SIMCA][SYNC]: delete :")
                    vv = VirtualServer.query.filter_by(name=existing_one.nomapp).first()
                    del_pool = Pools.query.filter_by(vs_id=vv.id).all()
                    for p in del_pool:
                        nn = Nodes.query.filter_by(id=p.id).all()
                        db.session.delete(p)
                        for n in nn:
                            db.session.delete(n)
                    db.session.delete(vv)
                    db.session.delete(existing_one)
                    db.session.commit()
        return "ok"
