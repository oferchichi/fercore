from f5.bigip import ManagementRoot
import urllib3
import requests
from prettytable import PrettyTable
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

class Recuperation():
    
    def __init__(self,ip,login,password):
        self.login = login
        self.password = password
        self.ip = ip
        self.mgmt = ManagementRoot(self.ip, self.login, self.password)
    
    def affichage(self):
        x = PrettyTable()
        x.field_names = ["VS_NAME", "POOL_NAME", "VS_VIP_IP" ,"VS_VIP_PORT" , "DESCRIPTION", "NODE_NAME", "NODE_PORT"]
        virs = self.mgmt.tm.ltm.virtuals.get_collection()
        for vir in virs:
            vs_name = vir.name
            if 'description' in vir.raw:
                description = vir.description
            else:
                description = None
            if 'destination' in vir.raw:
                destination = vir.destination.split('/')[2].split(':')[0]
                port_ecoute = vir.destination.split('/')[2].split(':')[1]
            if 'pool' in vir.sourceAddressTranslation:
                snatpool = vir.sourceAddressTranslation['pool']
            else:
                snatpool = None
            if 'pool' in vir.raw:
                    pool_name = vir.pool.split('/')[2]
                    pool = self.mgmt.tm.ltm.pools.pool.load(name=pool_name)
                    for member in pool.members_s.get_collection():
                        nodename = member.name.split(':')[0]
                        port = member.name.split(':')[1]
                        x.add_row([vs_name, pool_name, destination, port_ecoute, description, nodename,  port ])
        print(x)
            
R = Recuperation("126.246.24.147", "admin", "admin")
R.affichage()