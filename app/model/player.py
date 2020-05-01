from app.model.model import Model


class PlayerModel(Model):
    fields = ('id_player', 'username', 'password', 'date_created')
