from app.model.model import Model
import datetime


class GameModel(Model):
    fields = ('id_game', 'public_id', 'number_players',
              'date_created', 'date_started', 'date_finished')

    @classmethod
    def _update_date(cls, date, game_id):
        cls.update(
            {date: datetime.datetime.now()},
            ['id_game = %s', [game_id]]
        )

    @classmethod
    def start(cls, game_id):
        cls._update_date('date_started', game_id)

    @classmethod
    def end(cls, game_id):
        cls._update_date('date_finished', game_id)
