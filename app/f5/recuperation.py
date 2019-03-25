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

class Recuperation():

    def __init__(self, ip, login, password):
        self.login = login
        self.password = password
        self.ip = ip
        self.mgmt = ManagementRoot(self.ip, self.login, self.password)

    def affichage(self):
        x_application = PrettyTable()
        x_vs = PrettyTable()
        x_pool = PrettyTable()
        x_node = PrettyTable()
        type_application = AppType.query.all()
        environnement_application = Environnement.query.all()
        system_application = SystemInformation.query.all()
        x_application.field_names = ["APPLICATION_NAME", "STATUS", "FQDN", "DESCRIPTION", "CREATEUR",
                                     "SYSTEM_INF", "APPLICATION_TYPE", "ENVIRONNEMENT", "DISPONILITE", "TRIGRAM"]
        x_vs.field_names = ["VS_NAME", "PORT_SERVICE", "DESCRIPTION", "SOURCE_ADDRESS", "SNATPOOL", "IP_VIP",
                            "FULLPATH", "PARTITION"]
        x_pool.field_names = ["POOL_NAME", "PARTITION", "PORT", "FULLPATH"]
        x_node.field_names = ["NODE_NAME", "IP", "FULLPATH", "PARTITION"]
        virs = self.mgmt.tm.ltm.virtuals.get_collection()
        for vir in virs:
            vs_name = vir.name
            application_type = 42
            environnement_type = 42
            si_application = 42
            print("Name : {}".format(vir.name))
            if 'description' in vir.raw:
                description = vir.description
            else:
                description = None
            if 'destination' in vir.raw:
                destination = vir.destination.split('/')[2].split(':')[0]
                port_ecoute = vir.destination.split('/')[2].split(':')[1]
            else:
                destination = None
                port_ecoute = None
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
            if 'pool' in vir.raw:
                pool_name = vir.pool.split('/')[2]
                pool = self.mgmt.tm.ltm.pools.pool.load(name=pool_name)
                for member in pool.members_s.get_collection():
                    nodename = member.name.split(':')[0]
                    port = member.name.split(':')[1]
                    # app = Application(
                    #     nomapp=vs_name,
                    #     status="done",
                    #     fqdn=fqdn,
                    #     description=description,
                    #     createur=createur,
                    #     systeminformation=si_application,
                    #     trigram=trigram,
                    #     apptype=application_type,
                    #     environnement=environnement_type,
                    #     avability="1"
                    # )
                    # vs = VirtualServer(
                    #     name=vir.name,
                    #     fullpath=vir.fullPath,
                    #     portService=port_ecoute,
                    #     description=description,
                    #     sourceAddressTranslation=vir.sourceAddressTranslation['type'],
                    #     snatpool=snatpool,
                    #     partition="Common",
                    #     ipvip=destination,
                    #     equipement_id=Equipement.id,
                    #     app_id= app.id
                    # )
                    # pl = Pools(
                    #     name=pool_name,
                    #     fullpath=pool.fullpath,
                    #     partition="Common",
                    #     portService=port,
                    #     vs_id=vs.id
                    # )
                    # n= Nodes(
                    #     name=nodename,
                    #     ip=member.address,
                    #     fullname=member.name,
                    #     partition="Common",
                    #     pool_id=pl.id
                    # )
                    #     nomapp=vs_name,
                    #     status="done",
                    #     fqdn=fqdn,
                    #     description=description,
                    #     createur=createur,
                    #     systeminformation=si_application,
                    #     trigram=trigram,
                    #     apptype=application_type,
                    #     environnement=environnement_type,
                    #     avability="1"
                    x_application.add_row([vs_name, "done", fqdn, description, createur, si_application, trigram, application_type, environnement_type, "1"])
                    # x.add_row([vs_name, pool_name, destination, port_ecoute, description, nodename, port])
        return x_application
