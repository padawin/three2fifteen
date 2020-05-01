from flask import Blueprint, request, current_app
from app.controller.proxy import ProxyController
from app.controller.user import UserController
from app.controller.player import PlayerController
from app.service.proxy import ProxyService


bp = Blueprint('api', __name__)


@bp.route('/api/<string:service>',
          defaults={'path': ''},
          methods=ProxyService.valid_methods.keys())
@bp.route('/api/<string:service>/<path:path>',
          methods=ProxyService.valid_methods.keys())
def proxy(service, path):
    c = ProxyController(current_app.config)
    return c.execute(True, request, service, "/{}".format(path))

# Auth routes

@bp.route('/auth/sign-up', methods=['POST'])
def signup():
    c = UserController(current_app.config)
    return c.post(request)


@bp.route('/auth/login', methods=['POST'])
def login():
    c = UserController(current_app.config)
    return c.login(request)

# Social routes

@bp.route('/player/names/<string:id_users>', methods=['GET'])
def get_player_names(id_users):
    controller = PlayerController()
    return controller.get_names(request, id_users.split(','))
