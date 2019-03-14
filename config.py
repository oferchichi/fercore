import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'mysql://bpceit:bpceit123@localhost/appdb_final'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = False
    server = "http://126.246.28.228/"
    api_id = "automation"
    username = "Admin"
    password = "lsdbig99"
    baseurl = server + "/api/" + api_id
    section = 'Bunker-BPCEIT'
    sectionID = '3'
    ALBIRIO_PUBLIQUE = '16'
    ALBIRIO_DPUB = '12'
    ALBIRIO_DPRIV = '13'
    ANTARES_PUBLIQUE = '40'
    ANTARES_DPUB = '77'
    ANTARES_DPRIV = '64'
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
