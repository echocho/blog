from flask import Flask

import os

from blueprints.admin import admin_bp
from blueprints.auth import auth_bp
from blueprints.blog import blog_bp
from .extensions import bootstrap, db, mail, migrate, moment
from .settings import config


basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def create_app(config_name=None):
    if not config_name:
        config_name = os.getenv('FLASK_CONFIG_NAME', 'development')
    app = Flask('blog')
    app.config.from_object(config[config_name])

    configure_extensions(app)
    register_blueprints(app)
    return app


def configure_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    migrate.init_app(app, db)


def register_blueprints(app):
    app.register_blueprint(blog_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')
