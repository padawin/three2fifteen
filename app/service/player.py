from app.model.model import DuplicateFieldError
from werkzeug.security import generate_password_hash, \
                              check_password_hash


class PlayerService(object):
    EMPTY_NAME = 1
    NAME_TOO_LONG = 2
    USERNAME_ALREADY_USED = 3
    USERNAME_TOO_SHORT = 4
    USERNAME_TOO_LONG = 5
    PASSWORD_TOO_SHORT = 6

    INVALID_USERNAME = 1
    INVALID_PASSWORD = 2

    def __init__(self, model):
        self.model = model

    def get(self, username, password):
        user = self.model.loadBy({'username': username})
        if len(user) == 0:
            return (False, PlayerService.INVALID_USERNAME)
        if not check_password_hash(user[0]['password'], password):
            return (False, PlayerService.INVALID_PASSWORD)

        return (True, user[0])

    def create(self, username, password, name):
        name = name.strip()
        username = username.strip()
        password = password.strip()
        if len(username) == 0:
            return (False, PlayerService.USERNAME_TOO_SHORT)
        elif len(username) > 32:
            return (False, PlayerService.USERNAME_TOO_LONG)
        elif len(password) < 8:
            return (False, PlayerService.PASSWORD_TOO_SHORT)
        elif not len(name):
            return (False, PlayerService.EMPTY_NAME)
        elif len(name) > 128:
            return (False, PlayerService.NAME_TOO_LONG)

        try:
            player_id = self.model.insert({
                'username': username,
                'password': generate_password_hash(password),
                'name': name
            })
        except DuplicateFieldError:
            return (False, PlayerService.USERNAME_ALREADY_USED)
        else:
            return (True, player_id)

    def get_from_playerid(self, player_id):
        player = self.model.loadBy({'id_player': player_id})
        return player[0] if len(player) else None

    def get_names(self, player_ids):
        res = self.model.get_names(player_ids)
        names = {}
        for player in res:
            names[player['id_player']] = player['name']

        return names
