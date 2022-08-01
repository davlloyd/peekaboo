from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Client(db.Model):
    __tablename__ = 'client'
    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String(64), unique=True)
    ipaddress = db.Column(db.String(18), default=False, index=True)
    clients = db.relationship('client', backref='requests', lazy='dynamic')
    #db.session.add(clients)
    def __repr__(self):
        return '<Host_ID %r>' % self.id

class Request(db.Model):
    __tablename__ = 'requests'
    id = db.Column(db.Integer, primary_key=True)
    header = db.Column(db.Text)
    environment = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))

    def __repr__(self):
        return '<Request_ID %r>' % self.id
