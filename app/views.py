import socket
import os
from flask import request
from flask import jsonify
from flask import render_template
from app import app

@app.route('/', methods=["GET"])
def main():
    # Get general values
    hostname = socket.getfqdn()

    if request.remote_addr:
        requestip = request.remote_addr
    else:
        requestip = "Not Set"

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

    return render_template('index.html', requestip=requestip, xrealip=xrealip, headerdata=headerdata, hostname=hostname, xffheader=xffheader, environdata=environdata)

