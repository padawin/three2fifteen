from app.game import rules, score, board, bag
from app.model.model import Model


class TurnService(object):
    NO_GAME_FOUND = 1
    GAME_NOT_STARTED = 2
    GAME_FINISHED = 3
    WRONG_TURN_PLAYER = 4
    INVALID_PLAY_CONTENT = 5
    INVALID_PLAY_TOKEN = 6
    INVALID_PLAY_TYPE = 7
    CAN_STILL_PLAY = 8

    def __init__(self, game_model, turn_model, game_player_model):
        self.game_model = game_model
        self.turn_model = turn_model
        self.game_player_model = game_player_model

    def _get_bag(self, players, tokens_in_game):
        b = bag.Bag(
            [token['value'] for token in tokens_in_game]
            + [token for player in players for token in player['hand']]
        )
        return b

    def get_game_content(self, game_id):
        game = self.game_model.loadById(game_id)
        if game == {}:
            return None

        players = self.game_player_model.get_players(game_id)
        played_tokens = self.turn_model.get_game_content(game_id)
        bag = self._get_bag(players, played_tokens)
        return played_tokens, len(bag.tokens)

    def _pre_turn(self, game_id, player_id):
        game = self.game_model.loadById(game_id)
        if game is None:
            return (False, TurnService.NO_GAME_FOUND)
        elif game['date_started'] is None:
            return (False, TurnService.GAME_NOT_STARTED)
        elif game['date_finished'] is not None:
            return (False, TurnService.GAME_FINISHED)

        players = self.game_player_model.get_players(game_id)
        current_player = players[0]
        if current_player['id_player'] != player_id:
            return (False, TurnService.WRONG_TURN_PLAYER)
        return (True, (players, current_player))

    def turn(self, game_id, player_id, play, dry_run):
        (res, details) = self._pre_turn(game_id, player_id)
        if not res:
            return (False, details)
        (players, current_player) = details

        # test play is in player's hand
        for token in play:
            if not isinstance(token, dict):
                return (False, TurnService.INVALID_PLAY_TOKEN)
            if (
                not isinstance(token.get('value', None), int) or
                not isinstance(token.get('x', None), int) or
                not isinstance(token.get('y', None), int)
            ):
                return (False, TurnService.INVALID_PLAY_TYPE)
            if token['value'] not in current_player['hand']:
                return (False, TurnService.INVALID_PLAY_CONTENT)
            current_player['hand'].remove(token['value'])

        tokens_in_game = self.turn_model.get_game_content(game_id)
        current_board = board.Board(tokens_in_game)
        play_result = rules.analyse_play(current_board, play)
        if not play_result['valid']:
            return (False, play_result['reason'])

        score_play = score.calculate_score(current_board, play, play_result)
        values_play = [token['value'] for token in play]
        turn = {
            'id_game': game_id,
            'id_player': player_id,
            'x': [token['x'] for token in play],
            'y': [token['y'] for token in play],
            'value': values_play,
            'score': score_play
        }

        if not dry_run:
            self.turn_model.insert(turn)

            tokens_in_game += play
            # refill player's hand
            b = self._get_bag(players, tokens_in_game)
            hand = b.fill_hand(current_player['hand'])
            # update player's hand in DB
            self.game_player_model.set_points_and_hand(
                game_id,
                player_id,
                score_play,
                hand
            )
            # end of the game
            if len(hand) == 0 and b.is_empty():
                self.game_model.end(game_id)
                self.game_player_model.next_player(
                    current_player['id_game_player']
                )
            elif not any(current_board.is_bis(p['x'], p['y']) for p in play):
                self.game_player_model.next_player(
                    current_player['id_game_player'],
                    players[1]['id_game_player']
                )

            Model.commit()
        return (True, turn)

    def skip_turn(self, game_id, player_id, token_to_exchange, dry_run):
        (res, details) = self._pre_turn(game_id, player_id)
        if not res:
            return (False, details)
        (players, current_player) = details

        tokens_in_game = self.turn_model.get_game_content(game_id)
        board_instance = board.Board(tokens_in_game)
        if rules.can_play(board_instance, current_player['hand']):
            return (False, TurnService.CAN_STILL_PLAY)

        # remove token from hand
        if token_to_exchange not in current_player['hand']:
            return (False, TurnService.INVALID_PLAY_TOKEN)

        if not dry_run:
            current_player['hand'].remove(token_to_exchange)
            # Make sure it is not the same token which is picked
            b = self._get_bag(players, tokens_in_game)
            b.remove_same_tokens_as(token_to_exchange)
            if not b.is_empty():
                hand = b.fill_hand(current_player['hand'])
                self.game_player_model.set_points_and_hand(
                    game_id,
                    player_id,
                    0,
                    hand
                )
            self.game_player_model.next_player(
                current_player['id_game_player'],
                players[1]['id_game_player']
            )
            Model.commit()
        return (True, {})
