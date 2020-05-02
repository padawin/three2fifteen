from app.controller.controller import Controller
from app.service.player import PlayerService
from app.service.game import GameService
from app.service.turn import TurnService
from app.model.game import GameModel
from app.model.game_player import GamePlayerModel
from app.model.player import PlayerModel
from app.model.turn import TurnModel


class GameController(Controller):
    def __init__(self, request, identity):
        player_service = PlayerService(PlayerModel)
        self.player = player_service.get_from_playerid(identity['id_player'])
        if self.player is None:
            raise ValueError("Invalid player")

    def get(self, game_id):
        gs = GameService(GameModel, GamePlayerModel, PlayerModel)
        game = gs.get(game_id)
        if game is None:
            return self.format_response({'message': "No game found"}), 404
        game['players'][self.player['id_player']]['is_current'] = True
        self._format_date(game)
        return self.format_response(game)

    def _format_date(self, game):
        for date in ['date_created', 'date_started', 'date_finished']:
            game[date] = (game[date].isoformat() if game[date] else '')

    def get_all(self):
        gs = GameService(GameModel, GamePlayerModel, PlayerModel)
        games = gs.getPlayerGames(self.player['id_player'])
        for game in games:
            self._format_date(game)
            if game['players'][self.player['id_player']]['is_turn']:
                game['category'] = 'turn'
            elif game['date_started']:
                game['category'] = 'active'
            else:
                game['category'] = 'pending'
        return self.format_response(games)

    def post(self, request):
        data = request.get_json()
        needed_keys = ('number_players', )
        if data is None or any(k not in data for k in needed_keys):
            return self.format_response(
                {'message': "number_players required"}
            ), 400
        gs = GameService(GameModel, GamePlayerModel, PlayerModel)
        res = gs.create(self.player['id_player'], data['number_players'])
        players_count_message = "The number of players is invalid"
        unknown_player_message = "Unknown player ID"
        body, status = self.create_response(res, {
            0: lambda result: {'game_id': result},
            GameService.INVALID_NUMBER_PLAYERS: (players_count_message, 400),
            GameService.UNKNOWN_PLAYER: (unknown_player_message, 404)
        })
        return self.format_response(body), status

    def put_add_player(self, game_public_id):
        gs = GameService(GameModel, GamePlayerModel, PlayerModel)
        res = gs.addPlayer(game_public_id, self.player['id_player'])
        player_in_game_message = "You are already in the game"
        body, status = self.create_response(res, {
            GameService.NO_GAME_FOUND: ("No game found", 404),
            GameService.UNKNOWN_PLAYER: ("Unknown player ID", 404),
            GameService.GAME_FULL: ("The game is already full", 410),
            GameService.PLAYER_ALREADY_IN_GAME: (player_in_game_message, 400)
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

        gs = TurnService(GameModel, TurnModel, GamePlayerModel)
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
            0: lambda res: {'score': valid_score.format(res['score'])},
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
        ts = TurnService(GameModel, TurnModel, GamePlayerModel)
        content = ts.get_game_content(game_id)
        if content is None:
            return self.format_response({'message': "No game found"}), 404
        tokens, size_bag = content
        return self.format_response(
            {'tokens': tokens, 'size_bag': size_bag}
        )

    def get_hand(self, game_id):
        gs = GameService(GameModel, GamePlayerModel, PlayerModel)
        hand = gs.get_player_hand(game_id, self.player['id_player'])
        return self.format_response(hand)
