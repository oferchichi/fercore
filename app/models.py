from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)

    def __init__(self, username, password, email, group_id):
        self.username = username
        self.set_password(password)
        self.email = email
        self.group_id = group_id

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return {'id': self.id,
                'username': self.username,
                'email': self.email,
                'password': self.password_hash,
                'group_id': self.group_id
                }


class Group(db.Model):
    __tablename__ = 'group'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    users = db.relationship('User', backref='users')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return {
            'id': self.id,
            'name': self.name
        }


class PortStandardInternet(db.Model):
    __tablename__ = 'portStandardInternet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return {
            'id': self.id,
            'name': self.name
        }

class Equipement(db.Model):
    __tablename__ = 'equipement'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    ip = db.Column(db.String(80), nullable=False)
    port = db.Column(db.String(20))
    login = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    type_equipement = db.Column(db.String(80), nullable=False)
    fonction = db.Column(db.String(80), nullable=False)
    envi = db.Column(db.String(80), nullable=True)
    datacenter = db.Column(db.String(80), nullable=True)
    clusterName = db.Column(db.String(80), nullable=True)
    system_info = db.Column(db.Integer, db.ForeignKey('systeminformation.id'), nullable=False)
    virtualServer = db.relationship('VirtualServer', backref='virtualServer')
    reverseproxy = db.relationship('BeewereRp', backref='reverseproxy')
    couloirs = db.relationship('IcgCouloir', backref='couloir')
    
    def __init__(self, name, ip, port, login, password, fonction, type_equipement, datacenter, clusterName, sysuptime='', remarque=''):
        self.name = name
        self.ip = ip
        self.port = port
        self.login = login
        self.password = password
        self.sysuptime = sysuptime
        self.fonction = fonction
        self.remarque = remarque
        self.datacenter = datacenter
        self.clusterName = clusterName
        self.type_equipement = type_equipement

    def __repr__(self):
        return {
            'id': self.id,
            'name': self.name,
            'ip': self.ip,
            'port': self.port,
            'login': self.login,
            'password': self.password,
            'fonction': self.fonction,
            'type_equipement': self.type_equipement,
            'clusterName': self.clusterName,
            'datacenter': self.datacenter,
        }


class Application(db.Model):
    __tablename__ = 'application'
    id = db.Column(db.Integer, primary_key=True)
    nomapp = db.Column(db.String(80), unique=True, nullable=False)
    status = db.Column(db.String(80), nullable=False, default="pending")
    fqdn = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    createur = db.Column(db.String(200), nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    systeminformation = db.Column(db.Integer, db.ForeignKey('systeminformation.id'), nullable=False)
    trigram = db.Column(db.Integer, db.ForeignKey('trigram.id'), nullable=False)
    apptype = db.Column(db.Integer, db.ForeignKey('apptype.id'), nullable=False)
    environnement = db.Column(db.Integer, db.ForeignKey('environnement.id'), nullable=False)
    avability = db.Column(db.Integer, db.ForeignKey('avability.id'), nullable=False)
    virtualServerS = db.relationship('VirtualServer', backref='virtualServerS')
    tunnels = db.relationship('TunnelRp', backref='tunnels')

    def __init__(self, fqdn, nomapp, description, createur, systeminformation, trigram, apptype, environnement, avability, status='pending'):
        self.fqdn = fqdn
        self.nomapp = nomapp
        self.description = description
        self.createur = createur
        self.avability = avability
        self.systeminformation = systeminformation
        self.trigram = trigram
        self.apptype = apptype
        self.environnement = environnement
        self.status = status

    def __repr__(self):
        return {
            'id': self.id,
            'nomapp': self.nomapp,
            'fqdn': self.fqdn,
            'createur': self.createur,
            'description': self.description,
            'pub_date': self.pub_date,
            'systeminformation': self.systeminformation,
            'trigram': self.trigram,
            'apptype': self.apptype,
            'environnement': self.environnement,
            'avability': self.avability,
            'status': self.status
        }


class BeewereRp(db.Model):
    __tablename__ = 'reverseproxy'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=True, default="")
    qualification = db.Column(db.String(80), nullable=True)
    uidReverseProxy = db.Column(db.String(200), nullable=False)
    uidInterface = db.Column(db.String(200), nullable=False)
    ip = db.Column(db.String(80), nullable=False)
    rp_id = db.Column(db.Integer, db.ForeignKey('equipement.id'), nullable=False)

    def __init__(self, uidInterface, uidReverseProxy, ip, name, qualification):
        self.uidInterface = uidInterface
        self.uidReverseProxy = uidReverseProxy
        self.ip = ip
        self.qualification = qualification
        self.name = name

    def __repr__(self):
        return {
            'id': self.id,
            'name': self.name,
            'uidReverseProxy': self.uidReverseProxy,
            'uidInterface': self.uidInterface,
            'ip': self.ip,
            'qualification': self.qualification,
            'rp_id': self.rp_id
        }

class TunnelRp(db.Model):
    __tablename__ = 'tunnel'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    reverseproxy = db.Column(db.String(200), nullable=False)
    interface_incomming = db.Column(db.String(200), nullable=False)
    interface_outcomming = db.Column(db.String(200), nullable=False)
    portEntrer = db.Column(db.String(80), nullable=False)
    portSortie = db.Column(db.String(80), nullable=False)
    rp_id = db.Column(db.Integer, db.ForeignKey('equipement.id'), nullable=False)
    app_id = db.Column(db.Integer, db.ForeignKey('application.id'), nullable=True)

    def __repr__(self):
        return {
            'id': self.id,
            'name': self.name,
            'reverseproxy': self.reverseproxy,
            'interface_incomming': self.interface_incomming,
            'interface_outcomming': self.interface_outcomming,
            'portEntrer': self.portEntrer,
            'portSortie': self.portSortie,
            'rp_id': self.rp_id
        }

class Trigram(db.Model):
    __tablename__ = 'trigram'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    app_trigram = db.relationship('Application', backref='app_trigram')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return {
            'id': self.id,
            'name': self.name
        }


class SystemInformation(db.Model):
    __tablename__ = 'systeminformation'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    app_systemInformation = db.relationship('Application', backref='app_systemInformation')
    equipement_systemInformation = db.relationship('Equipement', backref='equipement_systemInformation')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return {
            'id': self.id,
            'name': self.name
        }


class AppType(db.Model):
    __tablename__ = 'apptype'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    app_appType = db.relationship('Application', backref='app_appType')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return {
            'id': self.id,
            'name': self.name
        }


class Environnement(db.Model):
    __tablename__ = 'environnement'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    app_environnement = db.relationship('Application', backref='app_environnement')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return {
            'id': self.id,
            'name': self.name
        }


class Avability(db.Model):
    __tablename__ = 'avability'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    app_avability = db.relationship('Application', backref='app_avability')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return {
            'id': self.id,
            'name': self.name
        }


class Ports(db.Model):
    __tablename__ = 'ports'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    used = db.Column(db.String(80), nullable=False)
    type_port = db.Column(db.String(80), nullable=False)
    nomapp = db.Column(db.String(80), nullable=True)

    def __init__(self, name, used, type_port, nomapp):
        self.name = name
        self.used = used
        self.type_port = type_port
        self.nomapp = nomapp

    def __repr__(self):
        return {
            'id': self.id,
            'name': self.name,
            'used': self.used,
            'type_port': self.type_port,
            'nomapp': self.nomapp
        }


class Nodes(db.Model):
    __tablename__ = 'nodes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=True)
    ip = db.Column(db.String(80), nullable=True)
    fullname = db.Column(db.String(80), nullable=True)
    partition = db.Column(db.String(80), nullable=True, default="Common")
    pool_id = db.Column(db.Integer, db.ForeignKey('pools.id'), nullable=True)

    def __repr__(self):
        return {
            'id': self.id,
            'name': self.name,
            'ip': self.ip,
            'fullname': self.fullname,
            'pool_id': self.pool_id,
        }


class Pools(db.Model):
    __tablename__ = 'pools'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=True)
    partition = db.Column(db.String(80), nullable=True, default="Common")
    portService = db.Column(db.String(80), nullable=True)
    fullpath = db.Column(db.String(80), nullable=True)
    nodes = db.relationship('Nodes', cascade="all,delete", backref='nodes')
    vs_id = db.Column(db.Integer, db.ForeignKey('virtualserver.id'), nullable=True)

    def __repr__(self):
        return {
            'id': self.id,
            'name': self.name,
            'portService': self.portService,
            'partition': self.partition,
            'fullpath': self.fullpath
        }


class VirtualServer(db.Model):
    __tablename__ = 'virtualserver'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    portService = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(80), nullable=False)
    sourceAddresstranslation = db.Column(db.String(80), nullable=False, default="None")
    snatPool = db.Column(db.String(80), nullable=False, default="None")
    ipvip = db.Column(db.String(80), nullable=False)
    fullpath = db.Column(db.String(80), nullable=False)
    partition = db.Column(db.String(80), nullable=False, default="Common")
    pools = db.relationship('Pools', cascade="all,delete", backref='pools')
    app_id = db.Column(db.Integer, db.ForeignKey('application.id'), nullable=False)
    equipement_id = db.Column(db.Integer, db.ForeignKey('equipement.id'), nullable=False)

    # def __repr__(self):
    #     return {
    #         'id': self.id,
    #         'name': self.name,
    #         'portService': self.portService,
    #         'description': self.description,
    #         'sourceAddresstranslation': self.sourceAddresstranslation,
    #         'ipvip': self.ipvip,
    #         'partition': self.partition,
    #         'snatPool': self.snatPool
    #     }


class GtmIp(db.Model):
    __tablename__ = 'gtmip'
    id = db.Column(db.Integer, primary_key=True)
    wide_ip = db.Column(db.String(80), unique=True, nullable=False)
    pub_antares = db.Column(db.String(80))
    pub_alberio = db.Column(db.String(80))
    dpub_alb = db.Column(db.String(80))
    dpub_ant = db.Column(db.String(80))
    dpriv_ant = db.Column(db.String(80))
    dpriv2_ant = db.Column(db.String(80))
    dpriv_alb = db.Column(db.String(80))
    dpriv2_alb = db.Column(db.String(80))
    reserverd_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    reserverd_par = db.Column(db.String(80))
    nomapp = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return {
            'id': self.id,
            'pub_antares': self.pub_antares,
            'dpub_ant': self.dpub_ant,
            'dpriv_ant': self.dpriv_ant,
            'dpriv2_ant': self.dpriv2_ant,
            'pub_alberio': self.pub_alberio,
            'dpub_alb': self.dpub_alb,
            'dpriv_alb': self.dpriv_alb,
            'dpriv2_alb': self.dpriv2_alb,
            'reserverd_on': self.reserverd_on,
            'reserverd_par': self.reserverd_par
        }


class Uptime(db.Model):
    __tablename__ = 'sysUptime'
    name = db.Column(db.String(100), primary_key=True)
    lastCheck = db.Column(db.String(100))
    status = db.Column(db.Integer)
    acknowledge = db.Column(db.Integer)
    comment = db.Column(db.String(100))

    def __repr__(self):
        return {
            'name': self.name,
            'lastCheck': self.lastCheck,
            'status': self.status,
            'acknowledge': self.acknowledge,
            'comment': self.comment
        }


class IcgCouloir(db.Model):
    __tablename__ = 'icgcouloir'
    id = db.Column(db.Integer, primary_key=True)
    cmd_exec = db.Column(db.String(200), nullable=False)
    destination = db.Column(db.String(80))
    namecouloir = db.Column(db.String(80))
    equipement_id = db.Column(db.Integer, db.ForeignKey('equipement.id'), nullable=True)    

    def __repr__(self):
            return {
                'id': self.id,
                'cmd_exec': self.cmd_exec,
                'destination': self.destination,
                'namecouloir': self.namecouloir,
                'equipement_id': self.equipement_id
            }
