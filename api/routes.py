from flask import Blueprint, request, current_app
from api.controller.player import PlayerController
from api.controller.game import GameController
from api.controller.board import BoardController
import api.plugin


bp = Blueprint('api', __name__, url_prefix="/api/")


# Auth routes

@bp.route('/login', methods=['POST'])
def login():
    c = PlayerController(current_app.config)
    return c.login(request)


# Debug routes

@bp.route('/games', methods=['GET'])
def get_games():
    from api.model import game
    return {"results": [game.dict() for game in game.games.values()]}


# Game routes

@bp.route('/board', methods=['GET'])
def get_board():
    controller = BoardController()
    return controller.get()


@bp.route('/game/<uuid:game_id>', methods=['GET'])
@api.plugin.need_auth
def get_game(game_id, identity):
    controller = GameController(current_app.config, request, identity)
    return controller.get(str(game_id))


@bp.route('/game/<uuid:game_id>/status', methods=['GET'])
@api.plugin.need_auth
def get_game_status(game_id, identity):
    controller = GameController(current_app.config, request, identity)
    return controller.get_status(str(game_id))


@bp.route('/game/<uuid:game_id>/content', methods=['GET'])
@api.plugin.need_auth
def get_game_content(game_id, identity):
    controller = GameController(current_app.config, request, identity)
    return controller.get_content(str(game_id))


#OK
@bp.route('/game', methods=['POST'])
@api.plugin.need_auth
def create_game(identity):
    controller = GameController(current_app.config, request, identity)
    return controller.post(request)


#OK
@bp.route('/game/<string:game_public_id>/join', methods=['PUT'])
@api.plugin.need_auth
def join_game(game_public_id, identity):
    controller = GameController(current_app.config, request, identity)
    return controller.put_add_player(game_public_id)


@bp.route('/game/<uuid:game_id>/turn/skip/check', methods=['PUT'])
@api.plugin.need_auth
def check_skip_turn_game(game_id, identity):
    raise ValueError()
    controller = GameController(current_app.config, request, identity)
    return controller.put_skip_turn(request, str(game_id), dry_run=True)


@bp.route('/game/<uuid:game_id>/turn/skip', methods=['PUT'])
@api.plugin.need_auth
def skip_turn_game(game_id, identity):
    raise ValueError()
    controller = GameController(current_app.config, request, identity)
    return controller.put_skip_turn(request, str(game_id), dry_run=False)


@bp.route('/game/<uuid:game_id>/turn/check', methods=['PUT'])
@api.plugin.need_auth
def check_turn_game(game_id, identity):
    controller = GameController(current_app.config, request, identity)
    return controller.put_turn(request, str(game_id), dry_run=True)


@bp.route('/game/<uuid:game_id>/turn', methods=['PUT'])
@api.plugin.need_auth
def turn_game(game_id, identity):
    controller = GameController(current_app.config, request, identity)
    return controller.put_turn(request, str(game_id), dry_run=False)


@bp.route('/game/<uuid:game_id>/hand', methods=['GET'])
@api.plugin.need_auth
def get_hand(game_id, identity):
    controller = GameController(current_app.config, request, identity)
    return controller.get_hand(str(game_id))
