from app.model.model import DuplicateFieldError, InvalidDataError, Model


class PlayerService(object):
    USER_ID_ALREADY_USED = 1
    INVALID_USER_ID = 2
    EMPTY_NAME = 3
    NAME_TOO_LONG = 4

    def __init__(self, model):
        self.model = model

    def create(self, user_id, name):
        name = name.strip()
        if not len(name):
            return (False, PlayerService.EMPTY_NAME)
        elif len(name) > 128:
            return (False, PlayerService.NAME_TOO_LONG)

        try:
            player_id = self.model.insert({
                'id_user': user_id,
                'name': name
            })
        except DuplicateFieldError:
            Model.rollback()
            return (False, PlayerService.USER_ID_ALREADY_USED)
        except InvalidDataError:
            Model.rollback()
            return (False, PlayerService.INVALID_USER_ID)
        Model.commit()
        return (True, player_id)

    def get_from_userid(self, user_id):
        player = self.model.loadBy({'id_user': user_id})
        return player[0] if len(player) else None
