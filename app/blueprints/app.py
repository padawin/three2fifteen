from flask import Blueprint, request, current_app
from app.controller.player import PlayerController
from app.controller.game import GameController
from app.controller.board import BoardController
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


# Game routes

@bp.route('/board', methods=['GET'])
def get_board():
    controller = BoardController()
    return controller.get()


@bp.route('/games', methods=['GET'])
@app.plugin.need_auth
def get_games(identity):
    controller = GameController(request, identity)
    return controller.get_all()


@bp.route('/game/<int:game_id>', methods=['GET'])
@app.plugin.need_auth
def get_game(game_id, identity):
    controller = GameController(request, identity)
    return controller.get(game_id)


@bp.route('/game/<int:game_id>/content', methods=['GET'])
@app.plugin.need_auth
def get_game_content(game_id, identity):
    controller = GameController(request, identity)
    return controller.get_content(game_id)


@bp.route('/game', methods=['POST'])
@app.plugin.need_auth
def create_game(identity):
    controller = GameController(request, identity)
    return controller.post(request)


@bp.route('/game/<string:game_public_id>/join', methods=['PUT'])
@app.plugin.need_auth
def join_game(game_public_id, identity):
    controller = GameController(request, identity)
    return controller.put_add_player(game_public_id)


@bp.route('/game/<int:game_id>/turn/skip/check', methods=['PUT'])
@app.plugin.need_auth
def check_skip_turn_game(game_id, identity):
    controller = GameController(request, identity)
    return controller.put_skip_turn(request, game_id, dry_run=True)


@bp.route('/game/<int:game_id>/turn/skip', methods=['PUT'])
@app.plugin.need_auth
def skip_turn_game(game_id, identity):
    controller = GameController(request, identity)
    return controller.put_skip_turn(request, game_id, dry_run=False)


@bp.route('/game/<int:game_id>/turn/check', methods=['PUT'])
@app.plugin.need_auth
def check_turn_game(game_id, identity):
    controller = GameController(request, identity)
    return controller.put_turn(request, game_id, dry_run=True)


@bp.route('/game/<int:game_id>/turn', methods=['PUT'])
@app.plugin.need_auth
def turn_game(game_id, identity):
    controller = GameController(request, identity)
    return controller.put_turn(request, game_id, dry_run=False)


@bp.route('/game/<int:game_id>/hand', methods=['GET'])
@app.plugin.need_auth
def get_hand(game_id, identity):
    controller = GameController(request, identity)
    return controller.get_hand(game_id)
