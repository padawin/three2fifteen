from app.model.model import Model


class PlayerModel(Model):
    fields = ('id_player', 'id_user', 'name', 'date_created')
