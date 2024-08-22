from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from main import config
import sys

db = SQLAlchemy()
app = Flask(__name__)

def create_app(config_name):
    app.config.from_object(config.config[config_name])
    config.config[config_name].init_app(app)
    db.init_app(app)

    app.logger.info('Import blueprints')
    from main.controllers import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

