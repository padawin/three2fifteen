from app.model.model import Model


class TurnModel(Model):
    fields = ('id_turn', 'id_game', 'id_player', 'x', 'y', 'value', 'score',
              'date_created')

    @classmethod
    def get_game_content(cls, game_id):
        query = """
        SELECT
            score,
            x,
            y,
            value
        FROM
            turn AS t
        WHERE
            id_game = %s
        """
        turns = cls.fetchAllRows(query, [game_id])
        played_tokens = []
        for turn in turns:
            for t in range(len(turn['x'])):
                played_tokens.append({
                    'x': turn['x'][t],
                    'y': turn['y'][t],
                    'value': turn['value'][t]}
                )

        return played_tokens
