import requests
import json
from config import Config


class Bee():

    def createBeewere(self, fqdn, nomapp, ipMgmt, portBeewere, portServiceEntrer, login, password, vipdorsal, portServiceSortie, uidBeewere, uidInterface, rp_id):
        print("[SIMCA][WORKFLOW][BEE]: Envoie de la requete vers le beewere: {}, => {}".format(ipMgmt, uidBeewere))
        url = "https://" + ipMgmt + ":" + portBeewere + "/wafapi/tunnels"
        payload = """
        {
            "name": "",
            "workflow": {
                "uid":"",
                "name":""
            },
            "reverseproxy": {
                "uid": ""
            },
            "network" : {
            "incoming": {
                    "interface": {
                        "uid": ""
                    },
                    "port": "",
                    "serverName": ""
                },
                "outgoing": {
                    "address": "",
                    "port": ""
            }
            },
            "monitor": {
                "enabled": false,
                "backend": {
                    "enabled": false
                }
            }
        }"""
        headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache"
        }
        data = json.loads(payload)
        data["name"] = nomapp
        data["reverseproxy"]["uid"] = uidBeewere
        if rp_id == "5":
            data["workflow"]["uid"] = "ISentryDefault"
            data["workflow"]["name"] = "WAF Default"
        else:
            data["workflow"]["name"] = Config.POLICY
        data["network"]["incoming"]["interface"]["uid"] = uidInterface
        data["network"]["incoming"]["port"] = portServiceEntrer
        data["network"]["incoming"]["serverName"] = fqdn
        data["network"]["outgoing"]["address"] = vipdorsal
        data["network"]["outgoing"]["port"] = portServiceSortie
        print("[SIMCA][WORKFLOW][BEE]: Chaine {},  IP ENTRER: {}".format(nomapp, uidInterface))
        print("[SIMCA][WORKFLOW][BEE]: Chaine {}, PORT ENTRER: {}".format(nomapp, portServiceEntrer))
        print("[SIMCA][WORKFLOW][BEE]: Chaine {}, IP SORTIE: {}".format(nomapp, vipdorsal))
        print("[SIMCA][WORKFLOW][BEE]: Chaine {}, PORT SORTIE {}".format(nomapp, portServiceSortie))
        response = requests.request("POST", url, auth=(login, password), verify=False, data=json.dumps(data), headers=headers)
        return response

    def rollbackBee(self, ip, login, password, port, tunnelName):
        print("[SIMCA][WORKFLOW][BEE]: Envoie de la requete pour supprimer un tunnel vers le beewere: {}, => {}".format(ip, tunnelName))
        url = "https://" + ip + ":" + port + "/wafapi/tunnels"
        payload = """
        {
            "name": ""
        }"""
        headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache"
        }
        data = json.loads(payload)
        data["name"] = tunnelName
        response = requests.request("DELETE", url, auth=(login, password), verify=False, data=json.dumps(data), headers=headers)
        if response.status_code == "200":
            print("[SIMCA][WORKFLOW][BEE]: Chaine {}  supprimer avec success".format(tunnelName))
            return "success"
        else:
            print("[SIMCA][WORKFLOW][BEE]: Erreur de suppression Chaine {} Merci de la faire maneullememnt code erreur {}, erreur : {}".format(tunnelName, str(response.status_code), response.json()))
            return "erreur"
