import uuid
import json
import random
import mysql.connector
from datetime import datetime

from api.game import bag


def connect(config):
    return mysql.connector.connect(
        host=config["DB_HOST"],
        user=config["DB_USER"],
        password=config["DB_PASSWORD"],
        database=config["DB_NAME"]
    )


class GameModel:
    def __init__(self, config):
        self.config = config
        self.id = None
        self.number_players = 0
        self.players = {}
        self.current_player = None
        self.played_tokens = []
        self.turn = 0
        self.date_created = datetime.now()
        self.date_started = None
        self.date_finished = None

    def dict(self):
        return {
            "id": self.id,
            "number_players": self.number_players,
            "count_players": len(self.players),
            "players": [
                {
                    "id_player": idx + 1,
                    "name": p["name"],
                    "points": p["points"],
                    "is_turn": p["is_turn"],
                    "is_current": self.current_player == p["id"]
                }
                for idx, p in enumerate(self.players.values())
            ],
            "played_tokens": self.played_tokens,
            "date_created": self.date_created,
            "date_started": self.date_started,
            "date_finished": self.date_finished
        }

    @classmethod
    def create(cls, number_players, config):
        game = cls(config)
        game.id = str(uuid.uuid1())
        game.number_players = number_players
        game.inserted = False
        game.save()
        return game

    @classmethod
    def loadById(cls, id, config):
        db = connect(config)
        cursor = db.cursor()
        sql = """
            SELECT
                number_players,
                players,
                current_player,
                played_tokens,
                turn,
                date_created,
                date_started,
                date_finished
            FROM
                game
            WHERE
                id = %s
        """

        cursor.execute(sql, (id,))

        result = cursor.fetchone()
        if result is None:
            return None
        game = cls(config)
        game.id = id
        game.inserted = True
        game.number_players = result[0]
        game.players = json.loads(result[1])
        game.current_player = result[2]
        game.played_tokens = json.loads(result[3])
        game.turn = result[4]
        game.date_created = result[5]
        game.date_started = result[6]
        game.date_finished = result[7]
        return game

    def add_player(self, player_id, player_name):
        self.players[player_id] = {
            "id": player_id,
            "name": player_name,
            "hand": [],
            'is_turn': False,
            'is_game_creator': len(self.players) == 0,
            'points': 0
        }
        self.save()

    def start(self):
        self.date_started = datetime.now()
        self.current_player = random.choice(list(self.players.keys()))
        self.players[self.current_player]["is_turn"] = True
        self.turn += 1
        # deal hands (starting from first player or in order of players?)
        b = bag.Bag()
        for player_id in self.players:
            self.set_player_hand(player_id, b.fill_hand())
        self.save()

    def set_player_hand(self, player_id, hand):
        self.players[player_id]["hand"] = hand

    def end(self):
        self.players[self.current_player]["points"] += self._sum_points_players_tokens()
        self.date_finished = datetime.now()
        self.save()

    def _sum_points_players_tokens(self):
        score = 0
        for pid, player in self.players.items():
            # No need to exclude current player, as their hand is empty (this
            # is called when a player finishes the game
            score += sum(token for token in player["hand"])
        return score

    def set_next_player(self):
        self.players[self.current_player]["is_turn"] = False
        player_ids = list(self.players.keys())
        current_player_index = player_ids.index(self.current_player)
        next_player_id = player_ids[(current_player_index + 1) % len(player_ids)]
        self.players[next_player_id]["is_turn"] = True
        self.current_player = next_player_id
        self.save()

    def do_turn(self, player_id, play, score_play):
        self.players[player_id]["points"] += score_play
        self.played_tokens.extend(play)
        self.turn += 1
        self.save()

    def save(self):
        db = connect(self.config)
        cursor = db.cursor()
        if not self.inserted:
            sql = """
                INSERT INTO
                    game (
                        number_players,
                        players,
                        current_player,
                        played_tokens,
                        turn,
                        id
                    ) VALUES (%s, %s, %s, %s, %s, %s)
                """
            val = (
                self.number_players,
                json.dumps(self.players),
                self.current_player,
                json.dumps(self.played_tokens),
                self.turn,
                self.id
            )
        else:
            sql = """
                UPDATE
                    game
                SET
                    players = %s,
                    current_player = %s,
                    played_tokens = %s,
                    turn = %s,
                    date_started = %s,
                    date_finished = %s
                WHERE
                    id = %s
                """
            val = (
                json.dumps(self.players),
                self.current_player,
                json.dumps(self.played_tokens),
                self.turn,
                self.date_started,
                self.date_finished,
                self.id
            )

        cursor.execute(sql, val)

        db.commit()
        self.inserted = True
