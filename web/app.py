from tornado.wsgi import WSGIContainer
from tornado.web import Application, FallbackHandler
from tornado.ioloop import IOLoop

import three2fifteen.factory
from three2fifteen import web_socket


def main():
    container = WSGIContainer(three2fifteen.factory.create_app())
    server = Application(
        [
            (r'/websocket/', web_socket.WebSocket),
            (r'.*', FallbackHandler, dict(fallback=container))
        ],
        autoreload=True
    )
    server.listen(5003)
    IOLoop.instance().start()


if __name__ == "__main__":
    main()
