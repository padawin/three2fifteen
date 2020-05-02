import logging
import jwt

from app.controller.controller import Controller
from app.model.model import Model
from app.model.player import PlayerModel
from app.service.player import PlayerService


class PlayerController(Controller):
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(config['APP_NAME'])

    def post(self, request):
        try:
            data = request.get_json()
        except BaseException:
            data = None

        if data is None or 'username' not in data or 'password' not in data or 'name' not in data:
            return self.format_response({
                'message': "name, username and password required"
            }), 400
        ps = PlayerService(PlayerModel)
        res = ps.create(data['username'], data['password'], data['name'])
        if res[0]:
            Model.commit()
        else:
            Model.rollback()

        user_exists_message = "A user already exists with this username"
        password_too_short = "The password must be at least 8 characters long"
        username_too_short = "The username is mandatory"
        username_too_long = "The username must be at most 32 characters long"
        empty_name = 'Your name can not be empty'
        name_too_long = 'We handle only name shorter than 128 characters'
        body, status = self.create_response(res, {
            0: lambda result: {'player_id': result},
            PlayerService.USERNAME_ALREADY_USED: (user_exists_message, 409),
            PlayerService.USERNAME_TOO_SHORT: (username_too_short, 400),
            PlayerService.USERNAME_TOO_LONG: (username_too_long, 400),
            PlayerService.PASSWORD_TOO_SHORT: (password_too_short, 400),
            PlayerService.EMPTY_NAME: (empty_name, 400),
            PlayerService.NAME_TOO_LONG: (name_too_long, 400),
        })
        return self.format_response(body), status

    def login(self, request):
        try:
            data = request.get_json()
        except BaseException:
            data = None

        if data is None or 'username' not in data or 'password' not in data:
            return self.format_response({
                'message': "username and password required"
            }), 400

        ps = PlayerService(PlayerModel)
        res = ps.get(**data)
        invalid_credentials = "Invalid username or password"
        body, status = self.create_response(res, {
            0: lambda result: {
                'access_token': jwt.encode({
                        'username': result['username'],
                        'id_player': result['id_player']
                    },
                    self.config['SECRET_KEY'],
                    algorithm='HS256'
                ).decode("utf-8")
            },
            PlayerService.INVALID_USERNAME: (invalid_credentials, 401),
            PlayerService.INVALID_PASSWORD: (invalid_credentials, 401)
        })
        return self.format_response(body), status

    def get_names(self, request, player_ids, identity):
        ps = PlayerService(PlayerModel)
        names = ps.get_names(player_ids)
        names[identity['id_player']] = 'You'
        return self.format_response(names)
