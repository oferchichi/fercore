import requests
from f5.bigip import ManagementRoot
import pycurl
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class F5():

    def connexion(login, password, ip):
        return ManagementRoot(ip, login, password)

    def createNode(connexion, node_ip, partition='Common'):
        try:
            connexion.tm.ltm.nodes.node.create(partition=partition, name=node_ip, address=node_ip)
            print("[SIMCA][Workflow][F5] : Node %s successfuly creer" % node_ip)
            return "success"
        except Exception:
            print("SIMCA][Workflow][F5]: Echec Creation de node" % node_ip)
            return "erreur"

    def delNode(connexion, nodeName, partition='Common'):
        if connexion.tm.ltm.nodes.node.exists(partition=partition, name=nodeName):
            node = connexion.tm.ltm.nodes.node.load(partition=partition, name=nodeName)
            node.delete()
            print("[SIMCA][Workflow][F5]: Node %s successfuly deleted" % nodeName)
            return "success"
        else:
            return "erreur"

    def createPool(connexion, poolName, partition, loadbalancing):
        if not connexion.tm.ltm.pools.pool.exists(partition=partition, name=poolName):
            connexion.tm.ltm.pools.pool.create(name=poolName, partition=partition, loadBalancingMode=loadbalancing)
            print("[SIMCA][Workflow][F5]: Pool %s successfuly created" % poolName)
            return "success"
        else:
            print("[SIMCA][Workflow][F5]: Pool %s existe deja" % poolName)
            return "erreur"

    def delPool(connexion, poolName, partition='Common'):
        if connexion.tm.ltm.pools.pool.exists(partition=partition, name=poolName):
            pool = connexion.tm.ltm.pools.pool.load(partition=partition, name=poolName)
            pool.delete()
            print("[SIMCA][Workflow][F5]: Pool %s successfuly deleted" % poolName)
        return "success"

    def AddNodeInPool(connexion, poolName, nodeName, fullname, partition='Common'):
        try:
            pool_b = connexion.tm.ltm.pools.pool.load(name=poolName, partition=partition)
            pool_b.members_s.members.create(partition='Common', name=fullname)
            pool_b.update()
            print("[SIMCA][Workflow][F5]: Ajout des nodes dans les pools")
            return "success"
        except Exception:
            return "erreur"

    def delNodeFromPool():
        return True

    def createVirtualServer(connexion, vsName, poolName, vipVS, port, profilesName, rulesName, ipProtocol, partition):
        if not connexion.tm.ltm.virtuals.virtual.exists(partition=partition, name=vsName):
            destination = vipVS + ':' + port
            vs = connexion.tm.ltm.virtuals.virtual.create(name=vsName, destination=destination,
                                                          pool=poolName, profiles=profilesName,
                                                          rules=rulesName, ipProtocol=ipProtocol, disabled=True,
                                                          partition=partition)
            print("[SIMCA][Workflow][F5]: VS %s successfuly created" % vs.name)
            return "success"
        else:
            print("[SIMCA][Workflow][F5]: VS %s existe deja" % vs.name)
            return "erreur"

    def delVirtualServer(connexion, vsName, partition):
        if connexion.tm.ltm.virtuals.virtual.exists(partition=partition, name=vsName):
            vs = connexion.tm.ltm.virtuals.virtual.load(partition=partition, name=vsName)
            vs.delete()
            print("[SIMCA][Workflow][F5]: VS %s successfuly deleted" % vsName)
            return "success"
        else:
            print("[SIMCA][Workflow][F5]: Erreur delete " % vsName)
            return "erreur"

    def suspendrePool(connexion, pool, pool_member, partition):
        try:
            print("[SIMCA][Workflow][F5]: Desactivation Node %s dans le pool" % pool_member)
            update_pool = connexion.tm.ltm.pools.pool.load(partition=partition, name=pool)
            update_pool_member = update_pool.members_s.load(partition=partition, name=pool_member)
            update_pool_member.session = "user-disabled"
            update_pool_member.state = "user-down"
            update_pool_member.description = "Node desactiver via SIMCA"
            update_pool_member.update()
            print("[SIMCA][Workflow][F5]: desactivation Node %s avec success" % pool_member)
            return "success"
        except Exception:
            print("[SIMCA][Workflow][F5]: Echec desactivation Node %s dans le pool" % pool_member)
            return "erreur"

    def suspendreNode(connexion, node, partition):
        try:
            print("[SIMCA][Workflow][F5]: Desactivation Node %s dans la globalite" % node)
            nodes = connexion.tm.ltm.nodes.node.load(partition=partition, name=node)
            nodes.session = "user-disabled"
            nodes.state = "user-down"
            nodes.update()
            print("[SIMCA][Workflow][F5]: desactivation Node %s avec success" % node)
            return "success"
        except Exception:
            print("[SIMCA][Workflow][F5]: Echec desactivation Node %s " % node)
            return "erreur"

    def changePool(connexion, vsName, newPool, partition):
        try:
            print("[SIMCA][Workflow][F5]: Modification de pool dans sont VS : %s " % vsName)
            vs = connexion.tm.ltm.virtuals.virtual.load(partition=partition, name=vsName)
            print("[SIMCA][Workflow][F5]: Modification du pool :%s par le pool : %s" % vs.pool, newPool)
            vs.pool = newPool
            vs.update()
            return "success"
        except Exception:
            print("[SIMCA][Workflow][F5]: Echec changement de Pool ")
            return "erreur"
