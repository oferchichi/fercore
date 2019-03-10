from flask import render_template, flash, redirect
from flask import Flask, request, jsonify, session
from flask_cors import CORS, cross_origin
from app import app
from app import db
from app.models import User, Group, Application, AppType, Avability, BeewereRp, Environnement
from app.models import Equipement, GtmIp, Pools, Ports, VirtualServer, Nodes, PortStandardInternet
from app.models import Uptime, SystemInformation, Trigram, TunnelRp

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Admin BPCEIT'}
    return render_template('index.html', title='Home', user=user)


@app.route('/api/register', methods=['POST'])
@cross_origin(supports_credentials=True)
def register():
    json_data = request.json
    print(json_data)
    groups = Group.query.filter_by(name=json_data['group']).first()
    if groups is None:
        return jsonify({"status": "Erreur creation Utilisateur Group non existant"})
    else:
        user = User(email=json_data['email'],
                    password=json_data['password'],
                    username=json_data['username'],
                    group_id=groups.id)
        try:
            db.session.add(user)
            db.session.commit()
            status = 'Utilisateur creer avec success'
        except Exception as e:
            db.session.rollback()
            return jsonify({"status": "Erreur creation Utilisateur "})
        db.session.close()
    return jsonify({'status': status})

@app.route('/api/login', methods=['POST'])
@cross_origin(supports_credentials=True)
def login():
    json_data = request.json
    username = json_data['username']
    password = json_data['password']
    groupname = ""
    user = User.query.filter_by(username=username).first()
    if user is None:
        return jsonify({'status': 'Erreur user/password not ok'})
    try:
        if user.check_password(password):
            group = Group.query.filter_by(id=user.group_id).first()
            groupname = group.name
            status = "True"
        else:
            return jsonify({'status': 'Erreur user/password not ok'})
    except Exception as e:
        status = "False :" + str(e)
    return jsonify({'status': status,
                    'username': user.username,
                    'group': groupname})

