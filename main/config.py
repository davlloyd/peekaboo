from operator import gt
import os
from os import path
import this
import sys
import uuid
from pyservicebinding import binding

basedir = os.getcwd()


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret'
    SESSION_COOKIE_HTTPONLY = False
    REQUEST_ID_UNIQUE_VALUE_PREFIX = "pab-"
    PERMANENT_SESSION_LIFETIME = 600
    WORKDIR = basedir
    ENV = 'unset'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite://'
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('DB_TRACK_MODIFICATIONS') or False
    BINDING_ROOT = "unset"

    try:
        _sb = binding.ServiceBinding()
        _db = _sb.bindings('mysql')
        BINDING_ROOT = "found"
    except binding.ServiceBindingRootMissingError:
        print("Environment Variable SERVICE_BINDING_ROOT not set")
        BINDING_ROOT = "unset"
    else:
        if _db:
            SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{_db[0]['username']}:{_db[0]['password']}@{_db[0]['host']}:{_db[0]['port']}/{_db[0]['database']}"
            print(f'Binding DB URI: {SQLALCHEMY_DATABASE_URI}')
        else:
            print('MySQL Binding not found, reverting to sqlite local store')


    @staticmethod
    def init_app(app):
        pass


class ProductionConfig(Config):
    ENV = 'production'
    if Config.SQLALCHEMY_DATABASE_URI is None:
        SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user@localhost/whatever'    

class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'
    if Config.SQLALCHEMY_DATABASE_URI is None:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')


class TestingConfig(Config):
    TESTING = True
    ENV = 'testing'
    if Config.SQLALCHEMY_DATABASE_URI is None:
        SQLALCHEMY_DATABASE_URI = 'sqlite://'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
