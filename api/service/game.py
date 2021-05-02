class GameService(object):
    GAME_FULL = 1
    NO_GAME_FOUND = 2
    PLAYER_ALREADY_IN_GAME = 3
    PLAYER_NAME_ALREADY_IN_GAME = 4

    INVALID_NUMBER_PLAYERS = 5
    UNKNOWN_PLAYER = 6

    def __init__(self, game_model, config):
        self.game_model = game_model
        self.config = config

    def get(self, game_id):
        return self.game_model.loadById(game_id, self.config)

    def get_player_hand(self, game_id, player_id):
        game = self.game_model.loadById(game_id, self.config)
        if game is None:
            return (False, GameService.NO_GAME_FOUND)
        player = game.players.get(player_id)
        if player is None:
            return (False, GameService.UNKNOWN_PLAYER)

        return (True, player["hand"])

    def create(self, player_id, player_name, number_players):
        try:
            number_players = int(number_players)
        except ValueError:
            return (False, GameService.INVALID_NUMBER_PLAYERS)

        if number_players < 2 or number_players > 4:
            return (False, GameService.INVALID_NUMBER_PLAYERS)

        game = self.game_model.create(number_players, self.config)
        game.add_player(player_id, player_name)
        return (True, game.id)

    def add_player(self, game_id, player_id, player_name):
        """
        Add a player to the game.
        Will return a tuple with a boolean as first value and an optional code
        as second value.
        If the player is added, the boolean will be True, othewise the boolean
        will be False and the code will be set
        """
        game = self.game_model.loadById(game_id, self.config)
        if game is None:
            return (False, GameService.NO_GAME_FOUND)

        if len(game.players) == game.number_players:
            return (False, GameService.GAME_FULL)
        elif any(pid for pid in game.players.keys() if pid == player_id):
            return (False, GameService.PLAYER_ALREADY_IN_GAME)
        elif any(p for p in game.players.values() if p["name"] == player_name):
            return (False, GameService.PLAYER_NAME_ALREADY_IN_GAME)

        game.add_player(player_id, player_name)

        if len(game.players) == game.number_players:
            game.start()

        return (True, None)
