import logging
from flask import Flask
from flask_cors import CORS
from werkzeug.utils import find_modules, import_string
import http.client as http_client


def create_app():
    app = Flask('three2fifteen-api')

    app.config.update({})
    app.config.from_envvar('THREE2FIFTEEN_API_SETTINGS', silent=False)

    logger = logging.getLogger("{} logger".format(app.name))
    logger.setLevel(logging.DEBUG)
    logging.info("starting server")

    register_logger()
    register_cors(app)
    register_blueprints(app)

    return app


def register_logger():
    http_client.HTTPConnection.debuglevel = 1
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True


def register_cors(app):
    CORS(app, origins=app.config['WEB_HOST'])


def register_blueprints(app):
    """Register all blueprint modules

    Reference: Armin Ronacher, "Flask for Fun and for Profit" PyBay 2016.
    """
    for name in find_modules('app.blueprints'):
        mod = import_string(name)
        if hasattr(mod, 'bp'):
            app.register_blueprint(mod.bp)
    return None
