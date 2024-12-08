import pkgutil

from flask import Flask, Blueprint
from importlib import import_module

import config


def _register_blueprints(flask_app, package_name, package_path):
    registered_bps = []
    for _, name, _ in pkgutil.iter_modules(package_path):
        module = import_module(f"{package_name}.{name}")
        for item in dir(module):
            item = getattr(module, item)
            if isinstance(item, Blueprint):
                flask_app.register_blueprint(item, url_prefix=f"/{item.name}")
                registered_bps.append(item)

    return registered_bps


def create_app(testing=False):
    app = Flask(__name__)
    _register_blueprints(app, __name__, __path__)
    app.config.from_object(config)

    return app
