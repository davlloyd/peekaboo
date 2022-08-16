from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from peekaboo import config
import sys
from flask_request_id_header.middleware import RequestID

db = SQLAlchemy()
app = Flask(__name__)


def create_app(config_name):
    app.config.from_object(config.config[config_name])
    config.config[config_name].init_app(app)
    RequestID(app)
    db.init_app(app)

    print('Import blueprints', file=sys.stdout)
    from peekaboo.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

