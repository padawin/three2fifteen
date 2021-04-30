import uuid
import logging
import os
import random
from os import path
from datetime import datetime
import pickle

from api.game import bag

games = dict()


def reset():
    games.clear()


def loadFromFile(gameID, config):
    games_directory = config["GAMES_STORAGE_DIR"]
    try:
        with open(path.join(games_directory, gameID), 'rb') as f:
            dumped = f.read()
    except FileNotFoundError:
        return None
    else:
        try:
            return pickle.loads(dumped)
        except pickle.UnpicklingError as e:
            logging.getLogger(__name__).error(e)
            return None


def saveToFile(game):
    games_directory = game.config["GAMES_STORAGE_DIR"]
    if not os.path.isdir(games_directory):
        os.makedirs(games_directory)
    with open(path.join(games_directory, game.id), 'wb') as f:
        f.write(pickle.dumps(game))


def deleteGameFile(game):
    games_directory = game.config["GAMES_STORAGE_DIR"]
    try:
        os.unlink(path.join(games_directory, game.id))
    except FileNotFoundError:
        pass


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
        games[game.id] = game
        game.save()
        return game

    @classmethod
    def loadById(cls, id, config):
        game = games.get(id)
        if game is None:
            game = loadFromFile(id, config)
            games[id] = game
        if game is not None:
            game.config = config
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
            self.fill_player_hand(player_id, b.fill_hand())
        self.save()

    def fill_player_hand(self, player_id, hand):
        self.players[player_id]["hand"] = hand

    def end(self):
        self.players[self.current_player]["points"] += self._sum_points_players_tokens()
        self.date_finished = datetime.now()
        self.delete()

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
        saveToFile(self)

    def delete(self):
        deleteGameFile(self)
