from flask import Blueprint, request, current_app
from app.controller.player import PlayerController
import app.plugin


bp = Blueprint('api', __name__)


# Auth routes

@bp.route('/auth/sign-up', methods=['POST'])
def signup():
    c = PlayerController(current_app.config)
    return c.post(request)


@bp.route('/auth/login', methods=['POST'])
def login():
    c = PlayerController(current_app.config)
    return c.login(request)


# Social routes

@bp.route('/player/names/<string:player_ids>', methods=['GET'])
@app.plugin.need_auth
def get_player_names(player_ids, identity):
    controller = PlayerController(current_app.config)
    return controller.get_names(request, player_ids.split(','), identity)
