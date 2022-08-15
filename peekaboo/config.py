from operator import gt
import os
from os import path
import this

from flask import current_app
basedir = os.getcwd()

class Binding:
    HOST = "localhost"
    USERNAME = "user"
    PASSWORD = "password"
    PORT = 3306
    DATABASE = "db"
    SQLALCHEMY_DATABASE_URI = ""
 
    def getDBURL(self, bindingFolder):    
        if path.exists(bindingFolder):
            i = 0
            for _key in os.listdir(bindingFolder):
                valueFile = bindingFolder + "/" + _key
                match _key:
                    case 'port':
                        self.PORT = open(valueFile).read()
                        i = i + 1
                    case 'database':
                        self.DATABASE = open(valueFile).read()
                        i = i + 1
                    case 'host':
                        self.HOST = open(valueFile).read()
                        i = i + 1
                    case 'username':
                        self.USERNAME = open(valueFile).read()
                        i = i + 1
                    case 'password':
                        self.PASSWORD = open(valueFile).read()
                        i = i + 1
            if i >= 4:
                self.SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{self.USERNAME}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}"
                return self.SQLALCHEMY_DATABASE_URI
            else:
                return None
        else:
            return None


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret'
    WORKDIR = basedir
    SERVICE_BINDING = 'peekaboo-binding'
    BINDING_ASSIGNED = False
    BINDING_FOLDER = WORKDIR + "/bindings/" + SERVICE_BINDING
    ENV = 'unset'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('DB_TRACK_MODIFICATIONS') or False

    @staticmethod
    def init_app(app):
        pass


class ProductionConfig(Config):
    ENV = 'production'
    if Config.SQLALCHEMY_DATABASE_URI is None:
        if path.exists(Config.BINDING_FOLDER):
            _binding = Binding()
            SQLALCHEMY_DATABASE_URI = _binding.getDBURL(Config.BINDING_FOLDER)
        else:
            SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user@localhost/whatever'    

class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'
    if Config.SQLALCHEMY_DATABASE_URI is None:
        if path.exists(Config.BINDING_FOLDER):
            _binding = Binding()
            SQLALCHEMY_DATABASE_URI = _binding.getDBURL(Config.BINDING_FOLDER)
        else:
            ##SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
            SQLALCHEMY_DATABASE_URI = 'sqlite:///'


class TestingConfig(Config):
    TESTING = True
    ENV = 'testing'
    if Config.SQLALCHEMY_DATABASE_URI is None:
        if path.exists(Config.BINDING_FOLDER):
            _binding = Binding()
            SQLALCHEMY_DATABASE_URI = _binding.getDBURL(Config.BINDING_FOLDER)
        else:
            SQLALCHEMY_DATABASE_URI = 'sqlite://'

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
