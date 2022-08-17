from email.header import Header
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from peekaboo import db, app
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.inspection import inspect
import json
import sys

print('Define DB Models', file=sys.stdout)

class Host(db.Model):
    __tablename__ = 'hosts'
    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String(64), unique=True, index=True)
    ostype = db.Column(db.Text)
    osversion = db.Column(db.Text)

    def __repr__(self):
        return self.id

    def add(self):
        _id = None
        db.session.add(self)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

        _resp = Host.query.with_entities(Host.id).filter(Host.hostname == self.hostname).first()
        _id = _resp["id"]

        return _id

    def get_id(self):
        _resp = Host.query.with_entities(Host.id).filter(Host.hostname == self.hostname).first()
        if(_resp is None):
            _id = self.add()
        else:
            _id = _resp["id"]
        return _id



class Request(db.Model):
    __tablename__ = 'requests'
    id = db.Column(db.Integer, primary_key=True)
    ipaddress = db.Column(db.String(18), default=False)
    xff = db.Column(db.Text)
    xrealip = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    requestid = db.Column(db.Text)
    host_id = db.Column(db.Integer, db.ForeignKey('hosts.id'))

    def __repr__(self):
        return self.id

    def add(self):
        _id = None
        db.session.add(self)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

        return self.id

    @staticmethod
    def get(requestid):
        _request = Request.query.filter(Request.id == requestid).all()
        return _request

    @staticmethod
    def get_history(hostid):
        _history = Request.query.filter(Request.host_id == hostid).all()
        return _history

    @staticmethod
    def get_dailycount_json():
        # Determining the structure between sqllite and mysql as schema context in queries vary
        _sql = "SELECT DATE(`timestamp`) AS 'date',COUNT(*) AS 'sessions' "
        _sql += "FROM requests "
        _sql += "GROUP BY DATE(`timestamp`);"
        _report = db.engine.execute(_sql)

        _json = []
        for _row in _report:
            if app.config['SQLALCHEMY_DATABASE_URI'].startswith('mysql'):
                _date = _row.date.isoformat()
            else:
                _date = _row.date
            _json.append({'Date': _date,
                          'Sessions': _row.sessions})
   
        return json.dumps(_json)



class Headers(db.Model):
    __tablename__ = 'headers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    value = db.Column(db.Text)
    request_id = db.Column(db.Integer, db.ForeignKey('requests.id'))

    def add(self):
        _id = None
        db.session.add(self)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

        return self.id

    @staticmethod
    def get_list(requestid):
        _list = Headers.query.filter(Headers.request_id == requestid).all()
        return _list


class WebEnvironment(db.Model):
    __tablename__ = 'web_environment'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    value = db.Column(db.Text)
    request_id = db.Column(db.Integer, db.ForeignKey('requests.id'))

    def add(self):
        _id = None
        db.session.add(self)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

        return self.id

    @staticmethod
    def get_list(requestid):
        _list = WebEnvironment.query.filter(WebEnvironment.request_id == requestid).all()
        return _list


class OSEnvironment(db.Model):
    __tablename__ = 'os_environment'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    value = db.Column(db.Text)
    request_id = db.Column(db.Integer, db.ForeignKey('requests.id'))

    def add(self):
        _id = None
        db.session.add(self)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

        return self.id

    @staticmethod
    def get_list(requestid):
        _list = OSEnvironment.query.filter(OSEnvironment.request_id == requestid).all()
        return _list


class JSONSerializer(json.JSONEncoder):
    @staticmethod
    def convert_if_date(_date):
        if isinstance(_date, datetime.date):
            return _date.strftime('%Y-%m-%d')
        return _date

    def date_insensitive_encode(self, obj):
        if isinstance(obj, dict):
            return {self.convert_if_date(k): v for k, v in obj.items()}
        return obj

    def encode(self, obj):
        return super(JSONSerializer, self).encode(
            self.date_insensitive_encode(obj))


print('DB URI: {0}'.format(app.config['SQLALCHEMY_DATABASE_URI']), file=sys.stdout)
print('Create DB', file=sys.stdout)
with app.app_context():
    db.create_all()
    db.session.commit()
