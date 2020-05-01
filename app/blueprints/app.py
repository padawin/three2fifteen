from flask import Blueprint, request, current_app
from app.controller.user import UserController
from app.controller.player import PlayerController
import app.plugin


bp = Blueprint('api', __name__)


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
@app.plugin.need_auth
def get_player_names(id_users, identity):
    controller = PlayerController()
    return controller.get_names(request, id_users.split(','))
