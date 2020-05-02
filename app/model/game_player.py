from app.model.model import Model


class GamePlayerModel(Model):
    fields = ('id_game_player', 'id_game', 'id_player', 'is_game_creator',
              'is_turn', 'hand', 'points', 'date_created')

    @classmethod
    def loadGamesFromPlayerId(cls, player_id):
        query = """
        SELECT
            g.id_game,
            public_id,
            number_players,
            g.date_created,
            g.date_started,
            g.date_finished,
            MAX(
                CASE
                    WHEN other_players.is_game_creator
                        THEN other_players.id_player
                END
            ) AS id_creator
        FROM game AS g
            INNER JOIN game_player AS curr_player
                ON g.id_game = curr_player.id_game
                    AND curr_player.id_player = %s
            INNER JOIN game_player AS other_players
                ON curr_player.id_game = other_players.id_game
            INNER JOIN player ON other_players.id_player = player.id_player
        WHERE
            public_id IS NOT NULL
            AND g.date_finished IS NULL
        GROUP BY
            g.id_game,
            public_id,
            number_players,
            g.date_created,
            g.date_started,
            g.date_finished
        ORDER BY
            (CASE
                WHEN date_finished IS NOT NULL THEN 3
                WHEN date_started IS NOT NULL THEN 1
                ELSE 2
            END) ASC,
            g.date_started DESC"""
        rows = cls.fetchAllRows(query, [player_id])
        return rows

    @classmethod
    def set_first_player(cls, game_id):
        c = cls._db.cursor()
        query = """UPDATE
            game_player
        SET
            is_turn = true
        WHERE id_game_player = (
            SELECT
                id_game_player
            FROM
                game_player
            WHERE
                id_game = %s
            ORDER BY random()
            LIMIT 1
        )"""
        c.execute(query.format(cls.getClass()), (game_id,))

    @classmethod
    def set_hand(cls, game_id, player_id, tokens):
        cls.update(
            {'hand': tokens},
            ['id_game = %s AND id_player = %s', [game_id, player_id]]
        )

    @classmethod
    def set_points_and_hand(cls, game_id, player_id, points, tokens):
        c = cls._db.cursor()
        query = """UPDATE
            game_player
        SET
            points = points + %s,
            hand = %s
        WHERE
            id_game = %s AND id_player = %s
        """
        c.execute(
            query.format(cls.getClass()),
            (points, tokens, game_id, player_id)
        )

    @classmethod
    def get_players(cls, game_id):
        """
        Returns all the players of a given game, with first the player whose
        turn it is
        """
        query = """
		SELECT
			gp.id_game_player AS id_game_player,
			gp.id_player AS id_player,
			gp.is_turn AS is_turn,
			gp.is_game_creator AS is_game_creator,
            gp.hand AS hand,
            gp.points AS points
		FROM
			game_player AS gp
            INNER JOIN player AS p ON gp.id_player = p.id_player
			LEFT JOIN
				game_player AS gpturn
				ON gpturn.id_game = %s AND gpturn.is_turn
		WHERE
			gp.id_game = %s
		ORDER BY
			gp.is_turn DESC,
			(CASE
				WHEN gp.date_created > gpturn.date_created THEN 1
				ELSE 2
			END) ASC
		"""
        rows = cls.fetchAllRows(query, [game_id, game_id])
        return rows

    @classmethod
    def next_player(cls, current_player, next_player=None):
        c = cls._db.cursor()
        query = "UPDATE \
            game_player \
        SET \
            is_turn = NOT is_turn \
        WHERE id_game_player in {}".format(
            "(%s, %s)"
            if next_player is not None
            else
            "(%s)"
        )
        c.execute(
            query.format(cls.getClass()),
            (current_player, next_player)
            if next_player is not None
            else
            (current_player,)
        )
