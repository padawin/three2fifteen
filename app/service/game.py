import uuid
from app.model.model import DuplicateFieldError, Model
from app.game import bag
from app.game import rules


class GameService(object):
    GAME_FULL = 1
    NO_GAME_FOUND = 2
    PLAYER_ALREADY_IN_GAME = 3

    INVALID_NUMBER_PLAYERS = 4
    UNKNOWN_PLAYER = 5

    def __init__(self, game_model, game_player_model, player_model):
        self.game_model = game_model
        self.game_player_model = game_player_model
        self.player_model = player_model

    def get(self, game_id):
        game = self.game_model.loadById(game_id)
        if game == {}:
            return None

        self._set_game_players(game)
        return game

    def get_player_hand(self, game_id, player_id):
        hand = self.game_player_model.loadBy(
            {'id_game': game_id, 'id_player': player_id}
        )
        if hand == []:
            return None

        return hand[0]['hand']

    def _set_game_players(self, game):
        players = self.game_player_model.get_players(game['id_game'])
        game['players'] = {}
        game['count_players'] = len(players)
        for player in players:
            game['players'][player['id_player']] = {
                'id_player': player['id_player'],
                'is_turn': player['is_turn'],
                'is_game_creator': player['is_game_creator'],
                'points': player['points']
            }

    def getPlayerGames(self, player_id):
        games = self.game_player_model.loadGamesFromPlayerId(player_id)
        for game in games:
            self._set_game_players(game)
        return games

    def _player_exists(self, player_id):
        player = self.player_model.loadBy({'id_player': player_id})
        return len(player) == 1

    def create(self, creator_player_id, number_players):
        try:
            number_players = int(number_players)
        except ValueError:
            return (False, GameService.INVALID_NUMBER_PLAYERS)

        if number_players < 2 or number_players > 4:
            return (False, GameService.INVALID_NUMBER_PLAYERS)

        if not self._player_exists(creator_player_id):
            Model.rollback()
            return (False, GameService.UNKNOWN_PLAYER)

        game_id = self.game_model.insert({
            "public_id": str(uuid.uuid1()),
            "number_players": number_players
        })
        self.game_player_model.insert({
            "id_game": game_id,
            "id_player": creator_player_id,
            "is_game_creator": True
        })
        Model.commit()
        return (True, game_id)

    def addPlayer(self, game_public_id, player_id):
        """
        Add a player to the game.
        Will return a tuple with a boolean as first value and an optional code
        as second value.
        If the player is added, the boolean will be True, othewise the boolean
        will be False and the code will be set
        """
        game = self.game_model.loadBy({'public_id': game_public_id})
        if not len(game):
            Model.rollback()
            return (False, GameService.NO_GAME_FOUND)

        game = game[0]
        game_id = game['id_game']
        if not self._player_exists(player_id):
            Model.rollback()
            return (False, GameService.UNKNOWN_PLAYER)

        players = self.game_player_model.loadBy({"id_game": game_id})
        nb_players = len(players)
        if nb_players == game['number_players']:
            Model.rollback()
            return (False, GameService.GAME_FULL)

        try:
            game_player_id = self.game_player_model.insert({
                "id_game": game_id,
                "id_player": player_id,
                "is_game_creator": False
            })
        except DuplicateFieldError:
            Model.rollback()
            return (False, GameService.PLAYER_ALREADY_IN_GAME)

        players.append({
            'id_game_player': game_player_id,
            'id_player': player_id
        })

        # The game is now full, can start
        if nb_players == game['number_players'] - 1:
            self._start(game_id, players)

        Model.commit()
        return (True,)

    def _start(self, game_id, players):
        self.game_model.start(game_id)
        self.game_player_model.set_first_player(game_id)
        # deal hands (starting from first player or in order of players?)
        b = bag.Bag()
        for player in players:
            self.game_player_model.set_hand(
                game_id,
                player['id_player'],
                b.fill_hand()
            )
