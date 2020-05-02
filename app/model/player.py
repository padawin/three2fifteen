from app.model.model import Model


class PlayerModel(Model):
    fields = ('id_player', 'username', 'password', 'name', 'date_created')

    @classmethod
    def get_names(cls, player_ids):
        query = """
        SELECT
            id_player,
            name
        FROM player
        WHERE
            id_player IN ({})
        """

        query = query.format(','.join(['%s'] * len(player_ids)))
        rows = cls.fetchAllRows(query, player_ids)
        return rows
