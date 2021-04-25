import uuid
import random
from datetime import datetime


games = dict()


class GameModel:
    def __init__(self):
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
    def create(cls, number_players):
        game = cls()
        game.id = str(uuid.uuid1())
        game.number_players = number_players
        games[game.id] = game
        return game

    @classmethod
    def loadById(cls, id):
        return games.get(id)

    def add_player(self, player_id, player_name):
        self.players[player_id] = {
            "id": player_id,
            "name": player_name,
            "hand": [],
            'is_turn': False,
            'is_game_creator': len(self.players) == 0,
            'points': 0
        }

    def start(self):
        self.date_started = datetime.now()
        self.current_player = random.choice(list(self.players.keys()))
        self.players[self.current_player]["is_turn"] = True
        self.turn += 1

    def end(self):
        self.date_finished = datetime.now()

    def set_next_player(self):
        self.players[self.current_player]["is_turn"] = False
        player_ids = list(self.players.keys())
        current_player_index = player_ids.index(self.current_player)
        next_player_id = player_ids[(current_player_index + 1) % len(player_ids)]
        self.players[next_player_id]["is_turn"] = True
        self.current_player = next_player_id
        self.turn += 1
