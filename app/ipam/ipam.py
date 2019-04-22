import requests
import json
from config import Config
from app.models import GtmIp, Ports
from app import db
import chardet

class Ipam:

    def get_token(self):
        res = requests.post(Config.baseurl + '/user/', auth=(Config.username, Config.password))
        retour = json.loads(res.content.decode(chardet.detect(res.content)["encoding"]))
        token = retour['data']['token']
        print("token: {}".format(token))
        return token

    def get_free_ip(self, subnetID):
        print("{}".format(subnetID))
        res = requests.get(Config.baseurl + '/addresses/first_free/' + subnetID, headers={'token': self.get_token()})
        data = json.loads(res.content.decode(chardet.detect(res.content)["encoding"]))
        if data:
            print("{}".format(data))
            return data['data']

    def del_reservation(self, ip):
        ipp = Ipam()
        res1 = requests.get(Config.baseurl + '/addresses/search/' + ip, headers={'token': ipp.get_token()})
        dd = json.loads(res1.content.decode(chardet.detect(res1.content)["encoding"]))
        if dd['success']:
            res = requests.delete(Config.baseurl + '/addresses/' + dd['data'][0]['id'], headers={'token': ipp.get_token()})
            d = json.loads(res.content.decode(chardet.detect(res.content)["encoding"]))
            if d:
                return d

    def set_ip_address(self, ip, description, hostname, createur, subnetID):
        res = requests.post(Config.baseurl + '/addresses/', headers={'token': self.get_token()}, params={'description': description, 'hostname': hostname, 'owner': createur, 'ip': ip,
                            'subnetId': subnetID, 'tag': '2'})
        d = json.loads(res.content.decode(chardet.detect(res.content)["encoding"]))
        if d:
            return d

    def reserve_ip_pour_qpa(self, createur, description, fqdn, nomapp):
        ipp = Ipam()
        try:
            elemenets = {}
            print("[SIMCA][WORKFLOW][IPAM] : Lancement de la reservation addressage IP pour << {} >> ".format(nomapp))
            print("{}  {}  {}".format(createur,description,fqdn))
            ip_public_qpa_ant = ipp.get_free_ip(Config.ANTARES_PUBLIQUE)
            print("[SIMCA][WORKFLOW][IPAM]: {}".format(ip_public_qpa_ant))
            ip_public_qpa_dpub = ipp.get_free_ip(Config.ANTARES_DPUB)
            print("[SIMCA][WORKFLOW][IPAM]: {}".format(ip_public_qpa_dpub))
            ip_public_qpa_dpriv = ipp.get_free_ip(Config.ANTARES_DPRIV)
            print("[SIMCA][WORKFLOW][IPAM]: {}".format(ip_public_qpa_dpriv))
            confirm_reservation_ip_public_qpa_ant = ipp.set_ip_address(ip_public_qpa_ant, description, fqdn, createur, Config.ANTARES_PUBLIQUE)
            confirm_reservation_ip_public_qpa_dpub = ipp.set_ip_address(ip_public_qpa_dpub, description, fqdn, createur, Config.ANTARES_DPUB)
            confirm_reservation_ip_public_qpa_dpriv = ipp.set_ip_address(ip_public_qpa_dpriv, description, fqdn, createur, Config.ANTARES_DPRIV)
            gtm = GtmIp(wide_ip=fqdn, pub_alberio="", pub_antares=ip_public_qpa_ant, dpriv2_ant="", dpriv_alb="", dpriv2_alb="", dpriv_ant=ip_public_qpa_dpriv,
                        dpub_alb="", dpub_ant=ip_public_qpa_dpub, reserverd_par=createur, nomapp=nomapp)
            try:
                db.session.add(gtm)
                db.session.commit()
                print("[SIMCA][WORKFLOW][IPAM] : Sauvgarde au niveau de la DB")
                elemenets['ip_public_qpa_ant'] = ip_public_qpa_ant
                elemenets['ip_public_qpa_dpub'] = ip_public_qpa_dpub
                elemenets['ip_public_qpa_dpriv'] = ip_public_qpa_dpriv
                elemenets['etat'] = "success"
            except Exception as e:
                db.session.rollback()
                print("[SIMCA][WORKFLOW][IPAM] : Erreur de sauvgarde rollback au niveau de la DB")
                ipp.del_reservation(ip_public_qpa_ant)
                ipp.del_reservation(ip_public_qpa_dpub)
                ipp.del_reservation(ip_public_qpa_dpriv)
                ipp.rollback_reservation_port(nomapp)
                print("[SIMCA][WORKFLOW][IPAM] : Rollback IP au niveau IPAM: {}".format(str(e)))
                elemenets['ip_public_qpa_ant'] = ''
                elemenets['ip_public_qpa_dpub'] = ''
                elemenets['ip_public_qpa_dpriv'] = ''
                elemenets['etat'] = "erreur"
            return elemenets
        except Exception as e:
            print("[SIMCA][WORKFLOW][IPAM] : Rollback IP au niveau IPAM effectuer : {}".format(str(e)))
            ipp.rollback_reservation_port(nomapp)

    def request_Port_Beewere_Internet(self, nomapp):
        print("[SIMCA][WORKFLOW][R PORT] : Lancement de la reservation pour port internet")
        ports_internet = Ports.query.filter_by(used='false', type_port='internet').first()
        ports_internet.nomapp = nomapp
        ports_internet.used = "true"
        elemenets = {}
        try:
            db.session.commit()
            print("[SIMCA][WORKFLOW][R PORT] : Port Pour Virtual Server Internet Reserver << {} >> ".format(ports_internet.name))
            elemenets['port_internet'] = ports_internet.name
            elemenets['etat'] = "success"
        except Exception as e:
            print("[SIMCA][WORKFLOW][R PORT] : Erreur reservation port  Virtual Server Internet ")
            print("[SIMCA][WORKFLOW][R PORT][ROLLBACK] : {}".format(str(e)))
            db.session.rollback()
            elemenets['port_internet'] = ''
            elemenets['etat'] = "erreur"
        return elemenets

    def request_Port_Beewere_Dorsal(self, nomapp):
        print("[SIMCA][WORKFLOW][R PORT] : Lancement de la reservation pour port dorsal")
        ports_dorsal = Ports.query.filter_by(used='false', type_port='dorsal').first()
        ports_dorsal.nomapp = nomapp
        ports_dorsal.used = "true"
        elemenets = {}
        try:
            db.session.commit()
            print("[SIMCA][WORKFLOW][R PORT] : Port Pour Virtual Server Dorsal Reserver << {} >> ".format(ports_dorsal.name))
            elemenets['port_dorsal'] = ports_dorsal.name
            elemenets['etat'] = "success"
        except Exception as e:
            print("[SIMCA][WORKFLOW][R PORT] : Erreur reservation port  Virtual Server Dorsal ")
            print("[SIMCA][WORKFLOW][R PORT][ROLLBACK] : {}".format(str(e)))
            db.session.rollback()
            elemenets['port_dorsal'] = ''
            elemenets['etat'] = "erreur"
        return elemenets

    def rollback_reservation_port(self, nomapp):
        print("[SIMCA][WORKFLOW][R PORT] : Rollback sur les ports")
        ports = Ports.query.filter_by(nomapp=nomapp).all()
        for port in ports:
            print("[SIMCA][WORKFLOW][R PORT] : Rollback port : {}".format(port.name))
            port.nomapp = ""
            port.used = "false"
            db.session.commit()

    def rollback_from_db(self, nomapp):
        try:
            print("[SIMCA][WORKFLOW][GTM] : Rollback sur enregistrement DB")
            gtm = GtmIp.query.filter_by(nomapp=nomapp).first()
            db.session.delete(gtm)
            db.session.commit()
        except Exception:
            print("[SIMCA][WORKFLOW][GTM] : Erreur Rollback sur enregistrement DB do it manualy")
