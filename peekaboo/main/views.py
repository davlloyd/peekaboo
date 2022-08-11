import datetime
import socket
import os
import time
from datetime import datetime
from flask import Blueprint, current_app, render_template, request, jsonify
from . import main,  session
from peekaboo import db
from peekaboo.data.models import Request, Client, Headers, OSEnvironment, WebEnvironment


_session = session.SessionData()

@main.route('/', methods=["GET"])
def home():
    if not _session.LOADED:
        _session.load()

    _requests = Request.get_dailycount_json()

    return render_template('home.html', requestip=_session.IPADDRESS, hostname=_session.FQDN, env=current_app.config['ENV'], dailyhits=_requests)

@main.route('/headers', methods=["GET"])
def headers():
    if not _session.LOADED:
        _session.load()

    return render_template('headers.html', xrealip=_session.XREALIP, headerdata=_session.HEADERS, xffheader=_session.XFF, osenvirondata=_session.OS_ENVIRONMENT, webenvirondata=_session.WEB_ENVIRONMENT)


@main.route('/variables', methods=["GET"])
def variables():
    if not _session.LOADED:
        _session.load()

    return render_template('variables.html', servervars=_session.OS_ENVIRONMENT)


@main.route('/time', methods=["GET"])
def timeInfo():
    if not _session.LOADED:
        _session.load()

    return render_template('response.html', servertime=datetime.now(), ticker=0) 

@main.route('/bindings', methods=["GET"])
def bindings():
    if not _session.LOADED:
        _session.load()
    
    return render_template('bindings.html', currentDir=os.getcwd(), bindingFound=_session.BINDINGFOUND, bindingvals=_session.BINDINGS, dburl=current_app.config['SQLALCHEMY_DATABASE_URI'])

@main.route('/history', methods=["GET", "POST"])
def history():
    _clients = Client.query.all()
    if request.method == "POST":
         _clientid = int(request.form["client"])
    else:
        if not _session.LOADED:
            _session.load()
        _clientid = _session.CLIENTID

    _requests = Request.get_history(_clientid)

    return render_template('history.html', clients=_clients, requests=_requests, clientid=_clientid)


@main.route('/history/<requestid>', methods=["GET"])
def history_request(requestid):
    if not _session.LOADED:
        _session.load()
    
    _request = Request.get(requestid)
    _headers = Headers.get_list(requestid)
    _osvars = OSEnvironment.get_list(requestid)
    _webvars = WebEnvironment.get_list(requestid)

    return render_template('history_details.html', request=_request[0], requestid=requestid, headers=_headers, osvars=_osvars, webvars=_webvars)

