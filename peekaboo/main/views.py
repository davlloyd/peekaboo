import datetime
import socket
import os
import time
from datetime import datetime
import flask
from flask import Blueprint, current_app, render_template, request, jsonify, session
from . import main, userdata
from peekaboo import db
from peekaboo.data.models import Request, Host, Headers, OSEnvironment, WebEnvironment

_sessions = {}

@main.route('/', methods=["GET"])
def home():
    current_app.logger.info("Views Request IP: %s",request.access_route[-1])

    _session = loadUserData()
    _requests = Request.get_dailycount_json()

    return render_template('home.html', dailyhits=_requests, fingerprint=_session.REQUESTID, requestip=_session.IPADDRESS)

@main.route('/node', methods=["GET"])
def node():
    _session = loadUserData()

    return render_template('node.html', requestip=_session.IPADDRESS, hostname=_session.FQDN, ostype=_session.OS_TYPE, 
                                        osversion=_session.OS_VERSION, env=current_app.config['ENV'])

@main.route('/headers', methods=["GET"])
def headers():
    _session = loadUserData()

    return render_template('headers.html', xrealip=_session.XREALIP, headerdata=_session.HEADERS, xffheader=_session.XFF, 
                                        osenvirondata=_session.OS_ENVIRONMENT, webenvirondata=_session.WEB_ENVIRONMENT)


@main.route('/variables', methods=["GET"])
def variables():
    _session = loadUserData()

    return render_template('variables.html', servervars=_session.OS_ENVIRONMENT)


@main.route('/time', methods=["GET"])
def timeInfo():
    _session = loadUserData()

    return render_template('response.html', servertime=datetime.now(), ticker=0) 

@main.route('/bindings', methods=["GET"])
def bindings():
    _session = loadUserData()

    return render_template('bindings.html', currentDir=os.getcwd(), 
                                    bindingFound=_session.BINDINGFOUND, bindingvals=_session.BINDINGS, 
                                    dburl=current_app.config['SQLALCHEMY_DATABASE_URI'], 
                                    bindingRoot=current_app.config['BINDING_ROOT'], 
                                    serviceBinding=current_app.config['SERVICE_BINDING'])

@main.route('/history', methods=["GET", "POST"])
def history():
    _hosts = Host.query.all()
    if request.method == "POST":
         _hostid = int(request.form["host"])
    else:
        _session = loadUserData()
        _hostid = _session.HOSTID

    _requests = Request.get_history(_hostid)

    return render_template('history.html', hosts=_hosts, requests=_requests, hostid=_hostid)


@main.route('/history/<requestid>', methods=["GET"])
def history_request(requestid):
    current_app.logger.info('Retrieving history for Request ID: %s', requestid)
    
    _request = Request.get(requestid)
    _headers = Headers.get_list(requestid)
    _osvars = OSEnvironment.get_list(requestid)
    _webvars = WebEnvironment.get_list(requestid)

    return render_template('history_details.html', request=_request[0], requestid=requestid, headers=_headers, osvars=_osvars, webvars=_webvars)

# Status query page, can also be used for the benchmark testing 
@main.route('/status', methods=["GET"])
def status():
    _status = {
        "health": "ok",
        "environment": current_app.config['ENV'],
        "database": current_app.config['SQLALCHEMY_DATABASE_URI'],
        "binding": current_app.config['BINDING_ASSIGNED']
    }
    return _status


# Persist user session data to DB and make accessible
def loadUserData():
    if session.get('fingerprint', None) is None or session['fingerprint'] not in _sessions:
        _session = userdata.SessionData()
        _session.load()
        _sessions[_session.REQUESTID] = _session
        session['fingerprint'] = _session.REQUESTID
    else:
        _session = _sessions[session['fingerprint']]
    
    return _session


