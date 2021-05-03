"""Atlas flask application module."""

import os

from flask import Flask
from werkzeug.utils import import_string

from corelibs import db
from . import config, io

def create_app(environment):
    """Create a new Flask application and initialize application."""
    app = Flask(__name__)
    app.env = environment
    app.config.from_object(config.Base())

    register_blueprints(app)
    io.init_app(app)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app


def register_blueprints(app):
    """
    Register module blueprints on given flask application.

    :param app: flask application
    """
    root_folder = 'api'

    for dir_name in os.listdir(root_folder):
        module_name = root_folder + '.' + dir_name + '.views'
        module_path = os.path.join(root_folder, dir_name, 'views.py')

        if os.path.exists(module_path):
            module = import_string(module_name)
            obj = getattr(module, 'app', None)
            if obj:
                obj.config = app.config
                app.register_blueprint(obj)
