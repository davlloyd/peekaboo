import socket
import os
import platform
from datetime import datetime
from flask import current_app, request
from . import main
from peekaboo import db, app
from peekaboo.data.models import Request, Host, OSEnvironment, Headers, WebEnvironment

class SessionData:
    LOADED = False
    FQDN = socket.getfqdn()
    IPADDRESS = "Not Set"
    HEADERS = {}
    XFF = "Not Set"
    WEB_ENVIRONMENT = {}
    OS_ENVIRONMENT = {}
    OS_TYPE = "Not Set"
    OS_VERSION = "Not Set"
    XREALIP = "Not Set"
    BINDINGFOUND = False
    BINDINGS = {}
    HOSTID = None

    # Load current runtime environment and session data
    def load(self):
        self.LOADED = True
        print("Session Request IP: {0}".format(request.remote_addr))
        if request.remote_addr:
            self.IPADDRESS = request.remote_addr
        self.OS_TYPE = platform.system()
        self.OS_VERSION = platform.platform()

        self.get_headerdata()
        self.get_environment()
        self.get_bindings()
        self.store_session()

    # Commit data from web session to the database 
    def store_session(self):
        # Commit key client data vie CLient model
        current = Host(hostname=self.FQDN, ostype=self.OS_TYPE, osversion=self.OS_VERSION)
        self.HOSTID=current.get_id()
        
        # Save request data within Request class model
        session = Request(
            ipaddress=self.IPADDRESS,
            xff=self.XFF,
            xrealip=self.XREALIP,
            host_id=self.HOSTID)
        
        _requestid = session.add()

        for _key in self.WEB_ENVIRONMENT:
            _env = WebEnvironment(
                name=_key,
                value=str(self.WEB_ENVIRONMENT[_key]),
                request_id=_requestid
            )
            _env.add()

        for _key in self.OS_ENVIRONMENT:
            _env = OSEnvironment(
                name=_key,
                value=str(self.OS_ENVIRONMENT[_key]),
                request_id=_requestid
            )
            _env.add()


        for _key in self.HEADERS:
            _header = Headers(
                name=_key,
                value=str(self.HEADERS[_key]),
                request_id=_requestid
            )
            _header.add()


        return True

    # Get header details from current session
    def get_headerdata(self):

        if request.headers:
            for _entry in request.headers:
                _key = _entry[0]
                _val = _entry[1]
                try:
                    self.HEADERS[_key]=_val
                except:
                    self.HEADERS[_key]="Exception occured"



            if request.headers.getlist("X-Forwarded-For"):
                self.XFF = request.headers.getlist("X-Forwarded-For")[0]
        

            # Get Header Values
            if request.environ.get('HTTP_X_REAL_IP'):
                self.XREALIP = request.environ.get('HTTP_X_REAL_IP')

        if request.environ:
            for _key in request.environ:
                try:
                    self.WEB_ENVIRONMENT[_key]=request.environ[_key]
                except:
                    self.WEB_ENVIRONMENT[_key]="Exception occured"


        return True

    # Get OS Environment details from current host
    def get_environment(self):
        for _key in os.environ:
            self.OS_ENVIRONMENT[_key] = os.environ[_key]
        return True


    # Read any service bindings assigned to system
    def get_bindings(self):
        if os.path.exists(app.config["BINDING_ROOT"]):
            self.BINDINGFOUND = True
            for _file in os.listdir(app.config["BINDING_ROOT"]):
                bindingFolder = app.config["BINDING_ROOT"] + _file
                self.BINDINGS["Binding"] = _file
                for _key in os.listdir(bindingFolder):
                    valueFile = bindingFolder + "/" + _key
                    if os.path.isfile(valueFile):
                        _value = open(valueFile)
                        self.BINDINGS[_key] = _value.read()
                        _value.close()
            return True
