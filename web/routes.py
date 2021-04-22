from flask import Blueprint, render_template, Response
from web.controller.config import ConfigController


bp = Blueprint(
    'three2fifteen',
    __name__,
    url_prefix="/",
    template_folder="templates",
)


@bp.route('/')
def index():
    return render_template('index.phtml')


@bp.route('/join/<uuid:game_id>')
def join_page(game_id):
    return render_template('game-join.phtml',
                           data=[{'key': 'game_id', 'value': game_id}])


@bp.route('/game/<uuid:game_id>')
def game_page(game_id):
    return render_template('game-page.phtml',
                           data=[{'key': 'game_id', 'value': game_id}])


@bp.route('/rules')
def rules():
    return render_template('rules.phtml')


@bp.route('/config.js')
def config():
    controller = ConfigController()
    return Response(render_template('config.js', data=controller.get()),
                    mimetype='application/javascript')
