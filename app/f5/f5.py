import requests
from f5.bigip import ManagementRoot
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

try:
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
except ImportError: 
    pass

class F5():

    def connexion(self, login, password, ip):
        return ManagementRoot(ip, login, password)

    def createNode(self, connexion, node_ip, partition='Common'):
        try:
            connexion.tm.ltm.nodes.node.create(partition=partition, name=node_ip, address=node_ip)
            print("[SIMCA][Workflow][F5] : Node %s successfuly creer" % node_ip)
            return "success"
        except Exception:
            print("SIMCA][Workflow][F5]: Echec Creation de node" % node_ip)
            return "erreur"

    def delNode(self, connexion, nodeName, partition='Common'):
        if connexion.tm.ltm.nodes.node.exists(partition=partition, name=nodeName):
            node = connexion.tm.ltm.nodes.node.load(partition=partition, name=nodeName)
            node.delete()
            print("[SIMCA][Workflow][F5]: Node %s successfuly deleted" % nodeName)
            return "success"
        else:
            return "erreur"

    def createPool(self, connexion, poolName, partition, loadbalancing):
        if not connexion.tm.ltm.pools.pool.exists(partition=partition, name=poolName):
            connexion.tm.ltm.pools.pool.create(name=poolName, partition=partition, loadBalancingMode=loadbalancing)
            print("[SIMCA][Workflow][F5]: Pool %s successfuly created" % poolName)
            return "success"
        else:
            print("[SIMCA][Workflow][F5]: Pool %s existe deja" % poolName)
            return "erreur"

    def delPool(self, connexion, poolName, partition='Common'):
        if connexion.tm.ltm.pools.pool.exists(partition=partition, name=poolName):
            pool = connexion.tm.ltm.pools.pool.load(partition=partition, name=poolName)
            pool.delete()
            print("[SIMCA][Workflow][F5]: Pool %s successfuly deleted" % poolName)
        return "success"

    def AddNodeInPool(self, connexion, poolName, nodeName, fullname, partition='Common'):
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

    def createVirtualServer(self, connexion, vsName, poolName, vipVS, port, profilesName, rulesName, ipProtocol, partition):
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

    def delVirtualServer(self, connexion, vsName, partition):
        if connexion.tm.ltm.virtuals.virtual.exists(partition=partition, name=vsName):
            vs = connexion.tm.ltm.virtuals.virtual.load(partition=partition, name=vsName)
            vs.delete()
            print("[SIMCA][Workflow][F5]: VS {} successfuly deleted".format(vsName))
            return "success"
        else:
            print("[SIMCA][Workflow][F5]: Erreur delete {} ".format(vsName))
            return "erreur"

    def suspendrePool(self, connexion, pool, pool_member, partition, action):
        try:

            print("[SIMCA][Workflow][F5]: Desactivation Node {} dans le pool".format(pool_member))
            update_pool = connexion.tm.ltm.pools.pool.load(partition=partition, name=pool)
            print("[SIMCA][Workflow][F5]: loaded pool {}".format(update_pool.name))
            update_pool_member = update_pool.members_s.members.load(partition=partition, name=pool_member)
            print("[SIMCA][Workflow][F5]: loaded pool members {}".format(update_pool_member.name))
            if action == "disable":
                update_pool_member.session = "user-disabled"
                update_pool_member.state = "user-down"
                update_pool_member.update()
            else:
                update_pool_member.session = "user-enabled"
                update_pool_member.state = "unchecked"
                update_pool_member.update()
            print("[SIMCA][Workflow][F5]: desactivation Node {} avec success".format(pool_member))
            return "success"
        except Exception as e:
            print("[SIMCA][Workflow][F5]: Echec desactivation Node {} dans le pool".format(pool_member))
            return "erreur"

    def suspendreNode(self, connexion, node, partition, action):
        try:
            print("[SIMCA][Workflow][F5]: Desactivation Node {} dans la globalite".format(node))
            nodes = connexion.tm.ltm.nodes.node.load(partition=partition, name=node)
            if action == 'disable':
                nodes.session = "user-disabled"
                nodes.state = "user-down"
                nodes.update()
            else:
                nodes.session = "user-enabled"
                nodes.state = "unchecked"
                nodes.update()
            print("[SIMCA][Workflow][F5]: desactivation Node {} avec success".format(node))
            return "success"
        except Exception as e:
            print("[SIMCA][Workflow][F5]: Echec desactivation Node {} : {}".format(node, str(e)))
            return "erreur"

    def changePool(self, connexion, vsName, newPool, partition):
        try:
            print("[SIMCA][Workflow][F5]: Modification de pool dans sont VS : {} ".format(vsName))
            vs = connexion.tm.ltm.virtuals.virtual.load(partition=partition, name=vsName)
            print("[SIMCA][Workflow][F5]: Modification du pool :{} par le pool : {}".format(vs.pool, newPool))
            vs.pool = newPool
            vs.update()
            return "success"
        except Exception as e:
            print("[SIMCA][Workflow][F5]: Echec changement de Pool {}".format(str(e)))
            return "erreur"

    def exec_cmd_bash(self, connexion, cmd):
        try:
            print("[SIMCA][Workflow][F5]: Changement de couloir : {} ".format(cmd))
            cmd_exec = "-c \'" + cmd + "\'"
            print("{}".format(cmd_exec))
            val = connexion.tm.util.bash.exec_cmd('run', utilCmdArgs=cmd_exec)
            return val.commandResult
        except Exception as e:
            print("[SIMCA][Workflow][F5]: Echec changement de Pool {}".format(str(e)))
            return "erreur"

