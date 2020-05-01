from werkzeug.security import generate_password_hash, \
                              check_password_hash
from app.model.model import DuplicateFieldError, Model
import logging


class UserService(object):
    USERNAME_ALREADY_USED = 1
    USERNAME_TOO_SHORT = 2
    USERNAME_TOO_LONG = 3
    PASSWORD_TOO_SHORT = 4
    ERROR_PLAYER_CREATION = 5
    INTERNAL_ERROR_PLAYER_CREATION = 6

    INVALID_USERNAME = 1
    INVALID_PASSWORD = 2

    def __init__(self, player_model, config):
        self.player_model = player_model
        self.logger = logging.getLogger(config['APP_NAME'])

    def get(self, username, password):
        user = self.player_model.loadBy({'username': username})
        if len(user) == 0:
            return (False, UserService.INVALID_USERNAME)
        if not check_password_hash(user[0]['password'], password):
            return (False, UserService.INVALID_PASSWORD)

        return (True, user[0])

    def create(self, username, password):
        username = username.strip()
        password = password.strip()
        if len(username) == 0:
            return (False, UserService.USERNAME_TOO_SHORT)
        elif len(username) > 32:
            return (False, UserService.USERNAME_TOO_LONG)
        elif len(password) < 8:
            return (False, UserService.PASSWORD_TOO_SHORT)

        try:
            user_id = self.player_model.insert({
                'username': username,
                'password': generate_password_hash(password)
            })
        except DuplicateFieldError:
            return (False, UserService.USERNAME_ALREADY_USED)
        else:
            return (True, user_id)
