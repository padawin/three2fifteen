from api.controller.controller import Controller
from api.model.game import GameModel
from api.service.game import GameService
from api.service.turn import TurnService


class GameController(Controller):
    def __init__(self, request, identity):
        self.player = identity

    def get_status(self, game_id):
        gs = GameService(GameModel)
        game = gs.get(game_id)
        if game is None:
            return self.format_response({'message': "No game found"}), 404
        return self.format_response({"current_turn": game.turn})

    def get(self, game_id):
        gs = GameService(GameModel)
        game = gs.get(game_id)
        if game is None:
            return self.format_response({'message': "No game found"}), 404
        response = game.dict()
        for idx, player_id in enumerate(game.players.keys()):
            if player_id == self.player['id_player']:
                response["players"][idx]['name'] = "You"
                break
        self._format_date(response)
        return self.format_response(response)

    def _format_date(self, game):
        for date in ['date_created', 'date_started', 'date_finished']:
            game[date] = (game[date].isoformat() if game[date] else '')

    def post(self, request):
        data = request.get_json()
        needed_keys = ('number_players', )
        if data is None or any(k not in data for k in needed_keys):
            return self.format_response(
                {'message': "number_players required"}
            ), 400
        gs = GameService(GameModel)
        res = gs.create(self.player['id_player'], self.player['username'], data['number_players'])
        players_count_message = "The number of players is invalid"
        body, status = self.create_response(res, {
            0: lambda result: {'game_id': result},
            GameService.INVALID_NUMBER_PLAYERS: (players_count_message, 400),
        })
        return self.format_response(body), status

    def put_add_player(self, game_id):
        gs = GameService(GameModel)
        res = gs.add_player(
            game_id, self.player["id_player"], self.player["username"]
        )
        player_in_game_message = "You are already in the game"
        duplicate_player_name_message = "There is already a player with this name"
        body, status = self.create_response(res, {
            GameService.NO_GAME_FOUND: ("No game found", 404),
            GameService.GAME_FULL: ("The game is already full", 410),
            GameService.PLAYER_ALREADY_IN_GAME: (player_in_game_message, 400),
            GameService.PLAYER_NAME_ALREADY_IN_GAME: (duplicate_player_name_message, 400)
        })
        return self.format_response(body), status

    def put_skip_turn(self, request, game_id, dry_run):
        data = request.get_json()
        needed_keys = ('token_to_discard', )
        if data is None or any(k not in data for k in needed_keys):
            return self.format_response(
                {'message': "token to exchange required"}
            ), 400

        gs = TurnService(GameModel, TurnModel, GamePlayerModel)
        res = gs.skip_turn(
            game_id,
            self.player['id_player'],
            data['token_to_discard'],
            dry_run
        )
        if not res[0] and isinstance(res[1], str):
            return self.format_response({'message': res[1]}), 400

        no_game = "No game found"
        game_not_started = "The game is not started"
        game_finished = "The game is finished"
        wrong_player_turn = "It is not your turn to play"
        invalid_play = "This token does not belong to you"
        invalid_token_format = "A token must be an integer"
        can_still_play = "You can play with your current hand"
        body, status = self.create_response(res, {
            0: lambda res: {},
            TurnService.NO_GAME_FOUND: (no_game, 404),
            TurnService.GAME_NOT_STARTED: (game_not_started, 403),
            TurnService.GAME_FINISHED: (game_finished, 410),
            TurnService.WRONG_TURN_PLAYER: (wrong_player_turn, 403),
            TurnService.INVALID_PLAY_CONTENT: (invalid_play, 400),
            TurnService.INVALID_PLAY_TYPE: (invalid_token_format, 400),
            TurnService.INVALID_PLAY_TOKEN: (invalid_token_format, 400),
            TurnService.CAN_STILL_PLAY: (can_still_play, 400)
        })
        return self.format_response(body), status

    def put_turn(self, request, game_id, dry_run):
        data = request.get_json()
        needed_keys = ('play', )
        if data is None or any(k not in data for k in needed_keys):
            return self.format_response(
                {'message': "play required"}
            ), 400

        gs = TurnService(GameModel)
        res = gs.turn(game_id, self.player['id_player'], data['play'], dry_run)
        if not res[0] and isinstance(res[1], str):
            return self.format_response({'message': res[1]}), 400

        no_game = "No game found"
        game_not_started = "The game is not started"
        game_finished = "The game is finished"
        wrong_player_turn = "It is not your turn to play"
        invalid_play = "Those tokens do not belong to you"
        invalid_token_format = ("A token must be a dict of integers with the "
                                "following keys: x, y, value")
        if dry_run:
            valid_score = "This play would give you {} points"
        else:
            valid_score = "You scored {} point"
        body, status = self.create_response(res, {
            0: lambda score: {'score': valid_score.format(score)},
            TurnService.NO_GAME_FOUND: (no_game, 404),
            TurnService.GAME_NOT_STARTED: (game_not_started, 403),
            TurnService.GAME_FINISHED: (game_finished, 410),
            TurnService.WRONG_TURN_PLAYER: (wrong_player_turn, 403),
            TurnService.INVALID_PLAY_CONTENT: (invalid_play, 400),
            TurnService.INVALID_PLAY_TYPE: (invalid_token_format, 400),
            TurnService.INVALID_PLAY_TOKEN: (invalid_token_format, 400)
        })
        return self.format_response(body), status

    def get_content(self, game_id):
        ts = TurnService(GameModel)
        content = ts.get_game_content(game_id)
        if content is None:
            return self.format_response({'message': "No game found"}), 404
        tokens, size_bag = content
        return self.format_response(
            {'tokens': tokens, 'size_bag': size_bag}
        )

    def get_hand(self, game_id):
        gs = GameService(GameModel)
        res = gs.get_player_hand(game_id, self.player['id_player'])
        body, status = self.create_response(res, {
            0: lambda hand: hand,
            GameService.NO_GAME_FOUND: ("No game faund", 404),
            GameService.UNKNOWN_PLAYER: ("Unkonwn player", 400),
        })
        return self.format_response(body), status
