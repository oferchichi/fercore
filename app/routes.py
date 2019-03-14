from flask import render_template, flash, redirect
from flask import Flask, request, jsonify, session
from flask_cors import CORS, cross_origin
from app import app
from app import db
from app.models import User, Group, Application, AppType, Avability, BeewereRp, Environnement
from app.models import Equipement, GtmIp, Pools, Ports, VirtualServer, Nodes, PortStandardInternet
from app.models import Uptime, SystemInformation, Trigram, TunnelRp
from app.f5.f5 import F5
from app.ipam.ipam import Ipam
from app.beewere.bee import Bee

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Admin BPCEIT'}
    return render_template('index.html', title='Home', user=user)


@app.route('/api/register', methods=['POST'])
@cross_origin(supports_credentials=True)
def register():
    json_data = request.json
    print(json_data)
    groups = Group.query.filter_by(name=json_data['group']).first()
    if groups is None:
        return jsonify({"status": "Erreur creation Utilisateur Group non existant"})
    else:
        user = User(email=json_data['email'],
                    password=json_data['password'],
                    username=json_data['username'],
                    group_id=groups.id)
        try:
            db.session.add(user)
            db.session.commit()
            status = 'Utilisateur creer avec success'
        except Exception as e:
            db.session.rollback()
            return jsonify({"status": "Erreur creation Utilisateur "})
        db.session.close()
    return jsonify({'status': status})

@app.route('/api/login', methods=['POST'])
@cross_origin(supports_credentials=True)
def login():
    json_data = request.json
    username = json_data['username']
    password = json_data['password']
    groupname = ""
    user = User.query.filter_by(username=username).first()
    if user is None:
        return jsonify({'status': 'Erreur user/password not ok'})
    try:
        if user.check_password(password):
            group = Group.query.filter_by(id=user.group_id).first()
            groupname = group.name
            status = "True"
        else:
            return jsonify({'status': 'Erreur user/password not ok'})
    except Exception as e:
        status = "False :" + str(e)
    return jsonify({'status': status,
                    'username': user.username,
                    'group': groupname})

@app.route('/api/application', methods=['POST'])
@cross_origin(supports_credentials=True)
def make_application_qpaf():
    ipammen = Ipam()
    print("[SIMCA][WORKFLOW][DB] : Creation du flow au niveau de la DB")
    print("[SIMCA][WORKFLOW][DB] : Generation automatique des noms des virtual server, pool, nodes et tunnels")
    json_data = request.json
    fqdn = json_data['fqdn']
    port_vs_internet = json_data['port_standard_internet']
    disponibiliter = json_data['ava']
    description = json_data['description']
    nomapp = json_data['nomapp']
    beewere_name = json_data['reverseproxy']
    system_information = json_data['si']
    trigram = json_data['trigram']
    environnement = json_data['env']
    type_profile = json_data['type']
    createur = json_data['createur']
    partition = 'Common'
    application_name = system_information + '-' + type_profile + '_' + nomapp.upper()
    print("[SIMCA][WORKFLOW][DB] : =======> Application : {}".format(application_name))
    port_internet = ipammen.request_Port_Beewere_Internet(application_name.upper())
    if port_internet['etat'] == 'erreur':
        return jsonify({'Etat': 'Erreur reservation des ports applicatif, merci de contacter votre administrateur systeme et verifier au niveau des la DB'})
    else:
        port_dorsal = ipammen.request_Port_Beewere_Dorsal(application_name.upper())
        if port_dorsal['etat'] == 'erreur':
            return jsonify({'Etat': 'Erreur reservation des ports applicatif, merci de contacter votre administrateur systeme et verifier au niveau des la DB'})
        else:
            try:
                ip_reservation = ipammen.reserve_ip_pour_qpa(createur, description, fqdn, application_name.upper())
            except Exception:
                ipammen.rollback_reservation_port(application_name.upper())
                ipammen.rollback_from_db(application_name.upper())
                return jsonify({'Etat': 'Erreur reservation des IP  applicatif rollback sur les ports, merci de contacter votre administrateur systeme et verifier au niveau des la DB'})
            if ip_reservation['etat'] == 'erreur':
                return jsonify({'Etat': 'Erreur reservation des IP  applicatif, merci de contacter votre administrateur systeme et verifier au niveau des la DB'})
            else:
                print("[SIMCA][WORKFLOW][DB] : Recuperation des objects de la DB ")
                object_System_information = SystemInformation.query.filter_by(name=system_information).first()
                object_Trigram = Trigram.query.filter_by(name=trigram).first()
                object_AppType = AppType.query.filter_by(name=type_profile).first()
                object_Environnement = Environnement.query.filter_by(name=environnement).first()
                object_Disponibliter = Avability.query.filter_by(name=disponibiliter).first()
                f5_internet_vs_name = environnement + '-' + system_information + '-' + type_profile + '_' + nomapp
                f5_internet_pool_name = environnement + '-' + system_information + '-' + type_profile + '_' + nomapp
                f5_dorsal_vs_name = environnement + '-' + system_information + '-' + type_profile + '_' + nomapp
                f5_dorsal_pool_name = environnement + '-' + system_information + '-' + type_profile + '_' + nomapp
                print("[SIMCA][WORKFLOW][DB] : =======> VirtualServer Internet : {}".format(f5_internet_vs_name))
                print("[SIMCA][WORKFLOW][DB] : =======> Pool Internet : {}".format(f5_internet_pool_name))
                print("[SIMCA][WORKFLOW][DB] : =======> VirtualServer Dorsal : {}".format(f5_dorsal_vs_name))
                print("[SIMCA][WORKFLOW][DB] : =======> Pool Dorsal : {}".format(f5_dorsal_pool_name))
                print("[SIMCA][WORKFLOW][DB] : Selection des equipements :")
                f5_internet_equipement_qpa = Equipement.query.filter_by(type_equipement="F5", fonction='internet', datacenter="ANT", envi="QPA").first()
                f5_dorsal_equipement_qpa = Equipement.query.filter_by(type_equipement="F5", fonction='dorsal', datacenter="ANT", envi="QPA").first()
                rp_tunnels_interface = BeewereRp.query.filter_by(qualification=beewere_name).all()
                print("[SIMCA][WORKFLOW][DB] : ======> f5_internet_equipement_qpa : {} ".format(f5_internet_equipement_qpa.ip))
                print("[SIMCA][WORKFLOW][DB] : ======> f5_dorsal_equipement_qpa : {} ".format(f5_dorsal_equipement_qpa.ip))
                print("[SIMCA][WORKFLOW][DB] : ======> f5_internet_equipement_qpa : {}, {} ".format(rp_tunnels_interface[0].ip, rp_tunnels_interface[1].ip))
                print("[SIMCA][WORKFLOW][DB] : Creation est ajout de lapplication au niveau de la DB ")
                app = Application(nomapp=application_name.upper(), fqdn=fqdn, description=description, createur=createur,
                                  systeminformation=object_System_information.id, trigram=object_Trigram.id, apptype=object_AppType.id,
                                  environnement=object_Environnement.id, avability=object_Disponibliter.id)
                try:
                    print("[SIMCA][WORKFLOW][DB] my test: {}".format(ip_reservation['ip_public_qpa_ant']))
                    db.session.add(app)
                    print("[SIMCA][WORKFLOW][DB] : Creation des Virtual Server et ajout dans la BD")
                    print("[SIMCA][WORKFLOW][DB] : Creation des Virtual Server Internet")
                    f5_VS_Internet = VirtualServer(name=f5_internet_vs_name.upper(), portService=port_vs_internet, ipvip=ip_reservation['ip_public_qpa_dpub'],
                                                   description=description, fullpath='/' + partition + '/' + f5_internet_vs_name.upper(), equipement_id=f5_internet_equipement_qpa.id, app_id=app.id)
                    print("[SIMCA][WORKFLOW][DB] : Creation des Virtual Server Dorsal")
                    f5_VS_Dorsal = VirtualServer(name=f5_dorsal_vs_name.upper(), portService=port_dorsal['port_dorsal'], ipvip=ip_reservation['ip_public_qpa_dpriv'],
                                                 description=description, equipement_id=f5_dorsal_equipement_qpa.id, fullpath='/' + partition + '/' + f5_dorsal_vs_name.upper(), app_id=app.id)
                    try:
                        print("SIMCA][WORKFLOW][DB] : {}".format(f5_VS_Internet.name))
                        db.session.add(f5_VS_Internet)
                        db.session.add(f5_VS_Dorsal)
                        print("[SIMCA][WORKFLOW][DB] : Commit Virtual OK")
                        print("[SIMCA][WORKFLOW][DB] : Start POOL CREATION F5 POOL INTERNET")
                        f5_POOL_Internet = Pools(name=f5_internet_pool_name.upper(),
                                                 portService=port_internet['port_internet'],
                                                 fullpath='/' + partition + '/' + f5_internet_pool_name.upper(),
                                                 vs_id=f5_VS_Internet)
                        print("[SIMCA][WORKFLOW][DB] : Start POOL CREATION F5 POOL DORSAL")
                        f5_POOL_Dorsal = Pools(name=f5_dorsal_pool_name.upper(),
                                               portService=port_dorsal['port_dorsal'],
                                               fullpath='/' + partition + '/' + f5_dorsal_pool_name.upper(),
                                               vs_id=f5_VS_Dorsal)
                        try:
                            db.session.add(f5_POOL_Internet)
                            db.session.add(f5_POOL_Dorsal)
                            print("[SIMCA][WORKFLOW][DB] : Start Tunnels")
                            i = 0
                            for interface_rp in rp_tunnels_interface:
                                nodes_internet = Nodes(name=interface_rp.ip,
                                                       ip=interface_rp.ip,
                                                       fullname=interface_rp.ip + ':' + port_internet['port_internet'],
                                                       pool_id=f5_POOL_Internet)
                                tunnels = TunnelRp(name=environnement + '-SR' + str(i) + '-WAF' + str(i) + '-' + system_information + '-' + type_profile + '_' + nomapp.upper(),
                                                   reverseproxy=interface_rp.uidReverseProxy,
                                                   interface_incomming=interface_rp.uidInterface,
                                                   interface_outcomming=f5_VS_Dorsal.ipvip,
                                                   portEntrer=f5_POOL_Internet.portService,
                                                   portSortie=f5_VS_Dorsal.portService,
                                                   rp_id=interface_rp.rp_id)
                                try:
                                    db.session.add(nodes_internet)
                                    db.session.add(tunnels)
                                    db.session.commit()
                                except Exception:
                                    db.session.rollback()
                                    raise MyErreur("Erreur Node ou Tunnel")
                                    return jsonify({'Etat': 'Erreur creation de la partie tunnels, merci de contacter votre administrateur systeme et verifier au niveau de la DB'})
                        except Exception as e:
                            db.session.rollback()
                            raise MyErreur("Erreur POOL")
                            return jsonify({'Etat': 'Erreur creation de la partie POOLL, merci de contacter votre administrateur systeme et verifier au niveau de la DB'})
                    except Exception as e:
                        db.session.rollback()
                        raise MyErreur("Erreur VS")
                        return jsonify({'Etat': 'Erreur creation de la partie virtual Server, merci de contacter votre administrateur systeme et verifier au niveau de la DB'})
                except (MyErreur, Exception):
                    db.session.rollback()
                    print("[SIMCA][WORKFLOW][DB] : Erreur de creation de lapplication au niveau de la DB, rollback en cours")
                    print("[SIMCA][WORKFLOW][DB] : Erreur de creation de lapplication au niveau de la DB :")
                    print("[SIMCA][WORKFLOW][DB] : Rollback reservation des IP")
                    ipammen.del_reservation(ip_reservation['ip_public_qpa_ant'])
                    ipammen.del_reservation(ip_reservation['ip_public_qpa_dpub'])
                    ipammen.del_reservation(ip_reservation['ip_public_qpa_dpriv'])
                    print("[SIMCA][WORKFLOW][DB] : Rollback reservation des Port")
                    ipammen.rollback_reservation_port(application_name.upper())
                    ipammen.rollback_from_db(application_name.upper())
                    return jsonify({'Etat': 'Erreur creation de la partie applicatif, merci de contacter votre administrateur systeme et verifier au niveau de la DB'})


class MyErreur(Exception):
    """ raise this erreur for any erruer"""
    pass
