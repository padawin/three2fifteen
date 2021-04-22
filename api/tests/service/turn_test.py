import pytest
import random
from unittest.mock import patch

from api.game import bag
from api.service import turn, game
from api.model.game import GameModel, games


def test_invalid_play_type():
    service = game.GameService(GameModel)
    _, game_id = service.create(1, "john", 2)
    service.add_player(game_id, 2, "doe")
    games[game_id].players[1]["is_turn"] = True
    games[game_id].players[2]["is_turn"] = False
    service = turn.TurnService(GameModel)
    fixtures = (
        ("foo", turn.TurnService.INVALID_PLAY_TOKEN),
        ({'x': 8, 'toto': 7, 'value': 4}, turn.TurnService.INVALID_PLAY_TYPE),
    )
    for play, result in fixtures:
        res = service.turn(game_id, 1, [play], dry_run=False)
        assert res == (False, result)


def test_wrong_turn_player():
    service = game.GameService(GameModel)
    _, game_id = service.create(1, "john", 2)
    service.add_player(game_id, 2, "doe")
    games[game_id].current_player = 1
    games[game_id].players[1]["is_turn"] = True
    games[game_id].players[2]["is_turn"] = False
    service = turn.TurnService(GameModel)
    res = service.turn(
        game_id,
        2,
        [
            {'x': 7, 'y': 7, 'value': 10},
            {'x': 8, 'y': 7, 'value': 4}
        ],
        dry_run=False
    )
    assert res == (False, turn.TurnService.WRONG_TURN_PLAYER)


@pytest.mark.parametrize(
    "hand, play",
    [
        [[1, 2, 3], [{'x': 1, 'y': 1, 'value': 4}, {'x': 1, 'y': 1, 'value': 5}]],
        [[1, 2, 4], [{'x': 1, 'y': 1, 'value': 1}, {'x': 1, 'y': 1, 'value': 1}]],
        [[1, 1, 1], [{'x': 1, 'y': 1, 'value': 1}, {'x': 1, 'y': 1, 'value': 2}]]
    ],
    ids=["Play different than hand",
         "Duplicate valid value",
         "Partly different"]
)
def test_play_not_in_hand(hand, play):
    service = game.GameService(GameModel)
    _, game_id = service.create(1, "john", 2)
    service.add_player(game_id, 2, "doe")
    games[game_id].current_player = 1
    games[game_id].players[1]["is_turn"] = True
    games[game_id].players[1]["hand"] = hand
    games[game_id].players[2]["is_turn"] = False
    service = turn.TurnService(GameModel)
    res = service.turn(
        game_id,
        1,
        play,
        dry_run=False
    )
    assert res == (False, turn.TurnService.INVALID_PLAY_CONTENT)


def test_turn_ok_next_player():
    service = game.GameService(GameModel)
    _, game_id = service.create(1, "john", 2)
    service.add_player(game_id, 2, "doe")
    games[game_id].current_player = 1
    games[game_id].players[1]["is_turn"] = True
    games[game_id].players[1]["hand"] = [10, 4, 5]
    games[game_id].players[2]["is_turn"] = False
    games[game_id].players[2]["hand"] = [10, 4, 5]
    service = turn.TurnService(GameModel)
    assert games[game_id].played_tokens == []
    assert games[game_id].players[1]["is_turn"] is True
    assert games[game_id].players[2]["is_turn"] is False
    res = service.turn(
        game_id,
        1,
        [
            {'x': 7, 'y': 7, 'value': 10},
            {'x': 8, 'y': 7, 'value': 4}
        ],
        dry_run=False
    )
    assert res == (True, 24)
    assert games[game_id].played_tokens == [
            {'x': 7, 'y': 7, 'value': 10},
            {'x': 8, 'y': 7, 'value': 4}
    ]
    assert games[game_id].players[1]["is_turn"] is False
    assert games[game_id].players[2]["is_turn"] is True


def test_turn_dry_run():
    service = game.GameService(GameModel)
    _, game_id = service.create(1, "john", 2)
    service.add_player(game_id, 2, "doe")
    games[game_id].current_player = 1
    games[game_id].players[1]["is_turn"] = True
    games[game_id].players[1]["hand"] = [10, 4, 5]
    games[game_id].players[2]["is_turn"] = False
    games[game_id].players[2]["hand"] = [10, 4, 5]
    service = turn.TurnService(GameModel)
    assert games[game_id].played_tokens == []
    assert games[game_id].players[1]["is_turn"] is True
    assert games[game_id].players[2]["is_turn"] is False
    res = service.turn(
        game_id,
        1,
        [
            {'x': 7, 'y': 7, 'value': 10},
            {'x': 8, 'y': 7, 'value': 4}
        ],
        dry_run=True
    )
    assert res == (True, 24)
    assert games[game_id].played_tokens == []
    assert games[game_id].players[1]["is_turn"] is True
    assert games[game_id].players[1]["hand"] == [10, 4, 5]
    assert games[game_id].players[2]["is_turn"] is False


@patch.object(bag.Bag, 'is_empty')
@patch.object(bag.Bag, 'fill_hand')
def test_turn_ok_end_game(mock_fillHand, mock_isEmpty):
    service = game.GameService(GameModel)
    _, game_id = service.create(1, "john", 2)
    service.add_player(game_id, 2, "doe")
    games[game_id].current_player = 1
    games[game_id].players[1]["is_turn"] = True
    games[game_id].players[1]["hand"] = [10, 4]
    games[game_id].players[2]["is_turn"] = False
    mock_isEmpty.return_value = True
    mock_fillHand.return_value = []
    # should return all the plays for the whole bag, minus the current play,
    # which in then emptying the bag
    service = turn.TurnService(GameModel)
    assert games[game_id].date_finished is None
    res = service.turn(
        game_id,
        1,
        [
            {'x': 7, 'y': 7, 'value': 10},
            {'x': 8, 'y': 7, 'value': 4}
        ],
        dry_run=False
    )
    assert res == (True, 24)
    assert games[game_id].date_finished is not None


def test_turn_ko():
    service = game.GameService(GameModel)
    _, game_id = service.create(1, "john", 2)
    service.add_player(game_id, 2, "doe")
    games[game_id].current_player = 1
    games[game_id].players[1]["is_turn"] = True
    games[game_id].players[1]["hand"] = [10, 4]
    games[game_id].players[2]["is_turn"] = False
    service = turn.TurnService(GameModel)
    res = service.turn(
        game_id,
        1,
        [
            {'x': 5, 'y': 7, 'value': 10},
            {'x': 8, 'y': 8, 'value': 4}
        ],
        dry_run=False
    )
    assert res[0] is False


def test_turn_unexisting_game():
    service = turn.TurnService(GameModel)
    res = service.turn(
        '123',
        '456',
        [
            {'x': 5, 'y': 7, 'value': 10},
            {'x': 8, 'y': 8, 'value': 4}
        ],
        dry_run=False
    )
    assert res == (False, turn.TurnService.NO_GAME_FOUND)
    res = service.skip_turn('123', '456', 10, dry_run=False)
    assert res == (False, turn.TurnService.NO_GAME_FOUND)


def test_turn_not_started_game():
    service = game.GameService(GameModel)
    _, game_id = service.create(1, "john", 2)
    service = turn.TurnService(GameModel)
    res = service.turn(
        game_id,
        1,
        [
            {'x': 5, 'y': 7, 'value': 10},
            {'x': 8, 'y': 8, 'value': 4}
        ],
        dry_run=False
    )
    assert res == (False, turn.TurnService.GAME_NOT_STARTED)
    res = service.skip_turn(game_id, 1, 10, dry_run=False)
    assert res == (False, turn.TurnService.GAME_NOT_STARTED)


def test_turn_game_already_finished():
    service = game.GameService(GameModel)
    _, game_id = service.create(1, "john", 2)
    service.add_player(game_id, 2, "doe")
    games[game_id].end()
    service = turn.TurnService(GameModel)
    res = service.turn(
        game_id,
        1,
        [
            {'x': 5, 'y': 7, 'value': 10},
            {'x': 8, 'y': 8, 'value': 4}
        ],
        dry_run=False
    )
    assert res == (False, turn.TurnService.GAME_FINISHED)
    res = service.skip_turn(game_id, 1, 10, dry_run=False)
    assert res == (False, turn.TurnService.GAME_FINISHED)


def test_turn_get_game_content_unknown_game():
    service = turn.TurnService(GameModel)
    res = service.get_game_content(123)
    assert res is None


@patch.object(random, 'choice')
def test_turn_get_game_content(mock_choice):
    mock_choice.side_effect = [
        # starting player
        1,
        # hand player 1
        10, 4, 3,
        # hand player 2
        10, 8, 7,
        # hand refil player 1
        1,
        # hand refil player 2
        2, 3
    ]
    service = game.GameService(GameModel)
    _, game_id = service.create(1, "john", 2)
    service.add_player(game_id, 2, "doe")
    service.add_player(game_id, 3, "tomo")
    service = turn.TurnService(GameModel)
    res = service.turn(game_id, 1, [{'x':7,'y':7,'value':3}], dry_run=False)
    assert res[0] is True
    assert games[game_id].players[1]["hand"] == [10, 4, 1]
    res = service.turn(game_id, 2, [{'x':7,'y':8,'value':8}, {'x':8,'y':8,'value':7}], dry_run=False)
    assert res[0] is True
    assert games[game_id].players[2]["hand"] == [10, 2, 3]
    played_tokens, size_bag = service.get_game_content(game_id)
    expected_tokens = [
        {'x': 7, 'y': 7, 'value': 3},
        {'x': 7, 'y': 8, 'value': 8},
        {'x': 8, 'y': 8, 'value': 7}
    ]
    assert size_bag == 72
    assert played_tokens == expected_tokens


@pytest.mark.parametrize(
    "player_hand, token_to_exchange, expected_result, dry_run",
    [
        [[0, 0, 0], 0, (False, turn.TurnService.CAN_STILL_PLAY), True],
        [[12, 15, 14], 10, (False, turn.TurnService.INVALID_PLAY_TOKEN), True],
        [[12, 15, 14], 14, (True, {}), True],
        [[0, 0, 0], 0, (False, turn.TurnService.CAN_STILL_PLAY), False],
        [[12, 15, 14], 10, (False, turn.TurnService.INVALID_PLAY_TOKEN), False],
        [[12, 15, 14], 14, (True, {}), False],
    ],
    ids=["Can still play, Dry run",
         "Invalid token, Dry run",
         "OK, Dry run",
         "Can still play",
         "Invalid token",
         "OK"]
)
def test_skip_turn(player_hand, token_to_exchange, expected_result, dry_run):
    service = game.GameService(GameModel)
    _, game_id = service.create(1, "john", 2)
    service.add_player(game_id, 2, "doe")
    games[game_id].played_tokens = [
        {"x": 7, "y": 7, "value": 12},
        {"x": 8, "y": 7, "value": 3},
        {"x": 7, "y": 8, "value": 1},
        {"x": 8, "y": 8, "value": 9}
    ]
    games[game_id].current_player = 1
    games[game_id].players[1]["is_turn"] = True
    games[game_id].players[1]["hand"] = player_hand
    games[game_id].players[2]["is_turn"] = False
    service = turn.TurnService(GameModel)
    res = service.skip_turn(game_id, 1, token_to_exchange, dry_run=dry_run)
    assert res == expected_result
    if res[0]:
        if dry_run:
            assert games[game_id].players[1]["hand"] == player_hand
        else:
            assert token_to_exchange not in games[game_id].players[1]["hand"]


@patch.object(bag.Bag, 'is_empty')
@patch.object(bag.Bag, 'fill_hand')
def test_skip_ok_end_game(mock_fillHand, mock_isEmpty):
    service = game.GameService(GameModel)
    _, game_id = service.create(1, "john", 2)
    service.add_player(game_id, 2, "doe")
    games[game_id].played_tokens = [
        {"x": 7, "y": 7, "value": 12},
        {"x": 8, "y": 7, "value": 3},
        {"x": 7, "y": 8, "value": 1},
        {"x": 8, "y": 8, "value": 9}
    ]
    games[game_id].current_player = 1
    games[game_id].players[1]["is_turn"] = True
    games[game_id].players[1]["hand"] = [12, 15, 14]
    games[game_id].players[2]["is_turn"] = False
    mock_isEmpty.return_value = True
    mock_fillHand.return_value = []
    # should return all the plays for the whole bag, minus the current play,
    # which in then emptying the bag
    service = turn.TurnService(GameModel)
    res = service.skip_turn(
        game_id,
        1,
        15,
        dry_run=False
    )
    assert res == (True, {})
    # The hand should be unchanged
    assert games[game_id].players[1]["hand"] == [12, 15, 14]
