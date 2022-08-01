from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from . import config
from app.main.session import main

app = Flask(__name__)
db = SQLAlchemy()

def create_app(config_name):
    app.config.from_object(config.config[config_name])
    config.config[config_name].init_app(app)
    db.init_app(app)

    app.register_blueprint(main)


    return app

