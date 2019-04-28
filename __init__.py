from flask import Flask

import os

from blog import config
from extensions import bootstrap, db, mail, moment
from blueprints import admin_bp, auth_bp, blog_bp

def create_app(config_name=None):
    if not config_name:
        config_name = os.getenv('FLASK_CONFIG_NAME', 'development')
    app = Flask('blog')
    app.config.from_object(config[config_name])

    configure_extensions(app)
    register_blueprints(app)

def configure_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    moment.init(app)

def register_blueprints(app):
    app.register_blueprint(blog_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')
