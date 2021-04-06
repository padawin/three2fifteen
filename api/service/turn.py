from api.game import rules, score, board, bag


class TurnService(object):
    NO_GAME_FOUND = 1
    GAME_NOT_STARTED = 2
    GAME_FINISHED = 3
    WRONG_TURN_PLAYER = 4
    INVALID_PLAY_CONTENT = 5
    INVALID_PLAY_TOKEN = 6
    INVALID_PLAY_TYPE = 7
    CAN_STILL_PLAY = 8

    def __init__(self, game_model):
        self.game_model = game_model

    def _get_bag(self, players, tokens_in_game):
        b = bag.Bag(
            [token['value'] for token in tokens_in_game]
            + [token for player in players.values() for token in player['hand']]
        )
        return b

    def get_game_content(self, game_id):
        game = self.game_model.loadById(game_id)
        if game is None:
            return None

        bag = self._get_bag(game.players, game.played_tokens)
        return game.played_tokens, len(bag.tokens)

    def _pre_turn(self, game_id, player_id):
        game = self.game_model.loadById(game_id)
        if game is None:
            return (False, TurnService.NO_GAME_FOUND)
        elif game.date_started is None:
            return (False, TurnService.GAME_NOT_STARTED)
        elif game.date_finished is not None:
            return (False, TurnService.GAME_FINISHED)

        current_player = game.players[player_id]
        if not current_player["is_turn"]:
            return (False, TurnService.WRONG_TURN_PLAYER)

        return (True, (game, current_player))

    def turn(self, game_id, player_id, play, dry_run):
        (res, details) = self._pre_turn(game_id, player_id)
        if not res:
            return (False, details)
        (game, current_player) = details

        # test play is in player's hand
        player_hand = current_player['hand'].copy()
        for token in play:
            if not isinstance(token, dict):
                return (False, TurnService.INVALID_PLAY_TOKEN)
            if (
                not isinstance(token.get('value', None), int) or
                not isinstance(token.get('x', None), int) or
                not isinstance(token.get('y', None), int)
            ):
                return (False, TurnService.INVALID_PLAY_TYPE)
            if token['value'] not in player_hand:
                return (False, TurnService.INVALID_PLAY_CONTENT)
            player_hand.remove(token["value"])

        current_board = board.Board(game.played_tokens)
        play_result = rules.analyse_play(current_board, play)
        if not play_result['valid']:
            return (False, play_result['reason'])

        score_play = score.calculate_score(current_board, play, play_result)
        if not dry_run:
            game.players[player_id]["points"] += score_play
            game.played_tokens.extend(play)
            for token in play:
                current_player['hand'].remove(token['value'])

            # refill player's hand
            b = self._get_bag(game.players, game.played_tokens)
            hand = b.fill_hand(current_player['hand'])

            game.players[player_id]["hand"] = hand
            if len(hand) == 0 and b.is_empty():
                # end of the game
                game.end()
            elif not any(current_board.is_bis(p['x'], p['y']) for p in play):
                game.set_next_player()

        return (True, score_play)

    def skip_turn(self, game_id, player_id, token_to_exchange, dry_run):
        (res, details) = self._pre_turn(game_id, player_id)
        if not res:
            return (False, details)
        (game, current_player) = details

        board_instance = board.Board(game.played_tokens)
        if rules.can_play(board_instance, current_player['hand']):
            return (False, TurnService.CAN_STILL_PLAY)

        # remove token from hand
        if token_to_exchange not in current_player['hand']:
            return (False, TurnService.INVALID_PLAY_TOKEN)

        if not dry_run:
            # Make sure it is not the same token which is picked
            b = self._get_bag(game.players, game.played_tokens)
            b.remove_same_tokens_as(token_to_exchange)
            if not b.is_empty():
                current_player['hand'].remove(token_to_exchange)
                hand = b.fill_hand(current_player['hand'])
                game.players[player_id]["hand"] = hand
            game.set_next_player()
        return (True, {})
