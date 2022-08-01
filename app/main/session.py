import datetime
import socket
import os
import time
from datetime import datetime
from flask import Blueprint, current_app, render_template, request, jsonify

main = Blueprint("main", __name__)

@main.route('/', methods=["GET"])
def home():
    # Get general values
    hostname = socket.getfqdn()

    if request.remote_addr:
        requestip = request.remote_addr
    else:
        requestip = "Not Set"

    return render_template('home.html', requestip=requestip, hostname=hostname, env=current_app.config['ENV'])

@main.route('/headers', methods=["GET"])
def headers():
    # Get general values

    if request.headers:
        headerdata=request.headers

        if request.headers.getlist("X-Forwarded-For"):
            xffheader = request.headers.getlist("X-Forwarded-For")[0]
        else:
            xffheader = "Not Set"
    
    else:
        headerdata = "Not Present"

    if request.environ:
        environdata = request.environ

        # Get Header Values
        if request.environ.get('HTTP_X_REAL_IP'):
            xrealip = request.environ.get('HTTP_X_REAL_IP')
        else:
            xrealip = "Not Set"

    else:
        environdata = "Not Set"

    return render_template('headers.html', xrealip=xrealip, headerdata=headerdata, xffheader=xffheader, environdata=environdata)


@main.route('/variables', methods=["GET"])
def variables():
    _vars={}
    for _key in os.environ:
        _vars[_key] = os.environ[_key]
    return render_template('variables.html', servervars=_vars)


@main.route('/time', methods=["GET"])
def timeInfo():
    servertime = datetime.utcnow()
    tupletime = servertime.timetuple()
    ticker = mktime(tupletime)
    return render_template('response.html', servertime=servertime, ticker=ticker) 

@main.route('/bindings', methods=["GET"])
def bindings():
    currentDir = os.getcwd()
    bindingFound = False
    bindingvals={}
    if os.path.exists("bindings"):
        bindingFound=True
        for _file in os.listdir('bindings'):
            bindingFolder = currentDir + "/bindings/" + _file
            bindingvals["Binding"] = _file
            for _key in os.listdir(bindingFolder):
                valueFile = bindingFolder + "/" + _key
                _value = open(valueFile)
                bindingvals[_key] = _value.read()
                _value.close()
    
    return render_template('bindings.html', currentDir=currentDir, bindingFound=bindingFound, bindingvals=bindingvals, dburl=current_app.config['SQLALCHEMY_DATABASE_URI'])

@main.errorhandler(404)
def page_not_found(_err):
    return render_template('404.html')

@main.errorhandler(500)
def page_not_found(_err):
    return render_template('500.html')
    