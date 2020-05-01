from flask import Blueprint, request, current_app
from app.controller.proxy import ProxyController
from app.service.proxy import ProxyService


bp = Blueprint('api', __name__)


@bp.route('/auth/<path:path>', methods=['POST'])
def login(path):
    c = ProxyController(current_app.config)
    return c.execute(False, request, 'auth', "/{}".format(path))


@bp.route('/api/<string:service>',
          defaults={'path': ''},
          methods=ProxyService.valid_methods.keys())
@bp.route('/api/<string:service>/<path:path>',
          methods=ProxyService.valid_methods.keys())
def proxy(service, path):
    c = ProxyController(current_app.config)
    return c.execute(True, request, service, "/{}".format(path))
