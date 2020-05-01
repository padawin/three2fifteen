import jwt

from app.model.player import PlayerModel
from app.service.user import UserService
from app.service.player import PlayerService
from app.controller.controller import Controller
from app.model.model import Model


class UserController(Controller):
    def __init__(self, config):
        self.config = config

    def post(self, request):
        try:
            data = request.get_json()
        except BaseException:
            data = None

        if data is None or 'username' not in data or 'password' not in data or 'name' not in data:
            return self.format_response({
                'message': "name, username and password required"
            }), 400
        us = UserService(PlayerModel, self.config)
        ps = PlayerService(PlayerModel, self.config)
        res = us.create(data['username'], data['password'])
        if res[0]:
            user_id = res[1]
            name = data['name']
            res = ps.create(user_id, name)
            if res[0]:
                Model.commit()
            else:
                Model.rollback()
        else:
            Model.rollback()

        user_exists_message = "A user already exists with this username"
        password_too_short = "The password must be at least 8 characters long"
        username_too_short = "The username is mandatory"
        username_too_long = "The username must be at most 32 characters long"
        empty_name = 'Your name can not be empty'
        name_too_long = 'We handle only name shorter than 128 characters'
        error_creation = 'An error occured during the creation of your account'
        body, status = self.create_response(res, {
            0: lambda result: {'player_id': result},
            UserService.USERNAME_ALREADY_USED: (user_exists_message, 409),
            UserService.USERNAME_TOO_SHORT: (username_too_short, 400),
            UserService.USERNAME_TOO_LONG: (username_too_long, 400),
            UserService.PASSWORD_TOO_SHORT: (password_too_short, 400),

            PlayerService.EMPTY_NAME: (empty_name, 400),
            PlayerService.NAME_TOO_LONG: (name_too_long, 400),
            PlayerService.USER_ID_ALREADY_USED: (error_creation, 500),
            PlayerService.INVALID_USER_ID: (error_creation, 500)
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

        ps = UserService(PlayerModel, self.config)
        res = ps.get(**data)
        invalid_credentials = "Invalid username or password"
        body, status = self.create_response(res, {
            0: lambda result: {
                'access_token': jwt.encode({
                        'username': result['username'],
                        'user_id': result['id_player']
                    },
                    self.config['SECRET_KEY'],
                    algorithm='HS256'
                ).decode("utf-8")
            },
            UserService.INVALID_USERNAME: (invalid_credentials, 401),
            UserService.INVALID_PASSWORD: (invalid_credentials, 401)
        })
        return self.format_response(body), status
