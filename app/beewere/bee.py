import pycurl
import requests
import json
from config import Config


class Bee():

    def createBeewere(fqdn, nomapp, ipMgmt, portBeewere, portServiceEntrer, login, password, vipdorsal, portServiceSortie, uidBeewere, uidInterface, rp_id):
        print("[*] [bee] : start chaine beewere")
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
        print(json.dumps(data))
        response = requests.request("POST", url, auth=(login, password), verify=False, data=json.dumps(data), headers=headers)
        return response
