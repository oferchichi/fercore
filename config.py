import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'mysql://bpceit:bpceit123@localhost/appdb_final'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = False
    server = "http://localhost/"
    api_id = "automation"
    username = "Admin"
    password = "ferchichi"
    baseurl = server + "/api/" + api_id
    section = 'BPCET-BUNKER'
    sectionID = '3'
    ALBIRIO_PUBLIQUE = '7'
    ALBIRIO_DPUB = '8'
    ALBIRIO_DPRIV = '9'
    ANTARES_PUBLIQUE = '10'
    ANTARES_DPUB = '11'
    ANTARES_DPRIV = '12'
    # F5 setting
    F5DORSAL_EXTENTION = ''
    F5INTERNET_EXTENTION = ''
    PROFILES = ['tcp', 'http']
    RULES = []
    PROTOCOLE_IP = 'tcp'
    LOADBALANCING_MODE = 'least-connections-member'
    PARTITION = 'Common'
    NODE_DORSAL_IP = '126.242.28.9'
    NODE_DORSAL_PORT = '80'
    DATACENTER_ALB_SAFIR = '_SAFIR'
    DATACENTER_ALB_TOPAZ = '_TOPAZ'
    DATACENTER_ANT_SIRUS = '_SIRUS'
    DATACENTER_ANT_VEGA = '_VEGA'
    # Reverse Proxy
    POLICY = 'I-Sentry Default'
    OUTGOING_PORT = '80'


class Develop(Config):
    SERVER_NAME = "localhost:8080"
