from app import db
from app.models import User, Group, Application, AppType, Avability, BeewereRp, Environnement
from app.models import Equipement, GtmIp, Pools, Ports, VirtualServer, Nodes, PortStandardInternet
from app.models import Uptime, SystemInformation, Trigram, TunnelRp

class Rollback:

    def rollback_app(self, nomapp):
        print("[SIMCA][WORKFLOW][APP] : Rollback sur enregistrement DB")
        app = Application.query.filter_by(nomapp=nomapp).first()
        virtualservers = VirtualServer.query.filter_by(app_id=app.id).all()
        for virtual in virtualservers:
            pool = Pools.query.filter_by(vs_id=virtual.id).first()
            nodes = Nodes.query.filter_by(pool_id=pool.id).all()
            for node in nodes:
                try:
                    db.session.delete(node)
                except Exception:
                    print("[SIMCA][WORKFLOW][APP] : Erreur Rollback sur enregistrement DB NODE")
            try:
                db.session.delete(pool)
                
            except Exception:
                print("[SIMCA][WORKFLOW][APP] : Erreur Rollback sur enregistrement DB Pool")
            try:
                db.session.delete(virtual)
            except Exception:
                print("[SIMCA][WORKFLOW][APP] : Erreur Rollback sur enregistrement DB VIR")
        try:
            db.session.delete(app)
            db.session.commit()
        except Exception:
            print("[SIMCA][WORKFLOW][APP] : Erreur sur enregistrement DB AOO")    
        return None
