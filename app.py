import logging
import os
from flask import Flask
import http.client as http_client
from tornado.wsgi import WSGIContainer
from tornado.web import Application, FallbackHandler
from tornado.ioloop import IOLoop

from websocket import websocket
from api.routes import bp as api_routes
from web.routes import bp as web_routes


def register_blueprints(app):
    app.register_blueprint(web_routes)
    app.register_blueprint(api_routes)


def register_logger():
    http_client.HTTPConnection.debuglevel = 1
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True


app = Flask('three2fifteen')

app.config.update({})
app.config.from_object('config.Config')
if os.environ.get("DEV"):
    app.config.from_object('config.DevConfig')

logger = logging.getLogger("{} logger".format(app.name))
logger.setLevel(logging.DEBUG)
logging.info("starting server")

register_blueprints(app)
register_logger()

container = WSGIContainer(app)
server = Application(
    [
        (r'/websocket/', websocket.WebSocket),
        (r'.*', FallbackHandler, dict(fallback=container))
    ],
    autoreload=True
)
application = server  # our hosting requires application in passenger_wsgi

if __name__ == "__main__":
    server.listen(5000)
    IOLoop.instance().start()
