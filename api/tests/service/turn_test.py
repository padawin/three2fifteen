import pytest
import random
from datetime import datetime
from unittest.mock import patch

from api.game import bag
from api.service import turn
from api.model.game import GameModel

config = {}


@pytest.mark.parametrize(
    "play, result",
    [
        ("foo", turn.TurnService.INVALID_PLAY_TOKEN),
        ({'x': 8, 'toto': 7, 'value': 4}, turn.TurnService.INVALID_PLAY_TYPE),
    ],
    ids=[
        "Invalid play token",
        "Invalid play type"
    ]
)
@patch.object(GameModel, "loadById")
def test_invalid_play_type(mock_loadById, play, result):
    game_id = '7fb8b876-a816-11e7-8b78-0469f8ed5e76'
    g = GameModel(config)
    g.id = game_id
    g.players = {
        1: {"id": 1, "name": "pierre", "hand": [1, 2, 3], "is_turn": True},
        2: {"id": 2, "name": "paul", "hand": [12, 13, 14], "is_turn": False}
    }
    g.number_players = 2
    g.current_player = 1
    g.date_started = datetime.now()
    mock_loadById.return_value = g
    service = turn.TurnService(GameModel, config)
    res = service.turn(game_id, 1, [play], dry_run=False)
    assert res == (False, result)


@patch.object(GameModel, "loadById")
def test_wrong_turn_player(mock_loadById):
    game_id = '7fb8b876-a816-11e7-8b78-0469f8ed5e76'
    g = GameModel(config)
    g.id = game_id
    g.players = {
        1: {"id": 1, "name": "pierre", "hand": [1, 2, 3], "is_turn": True},
        2: {"id": 2, "name": "paul", "hand": [12, 13, 14], "is_turn": False}
    }
    g.number_players = 2
    g.current_player = 1
    g.date_started = datetime.now()
    mock_loadById.return_value = g
    service = turn.TurnService(GameModel, config)
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
@patch.object(GameModel, "loadById")
def test_play_not_in_hand(mock_loadById, hand, play):
    game_id = '7fb8b876-a816-11e7-8b78-0469f8ed5e76'
    g = GameModel(config)
    g.id = game_id
    g.players = {
        1: {"id": 1, "name": "pierre", "hand": hand, "is_turn": True},
        2: {"id": 2, "name": "paul", "hand": [12, 13, 14], "is_turn": False}
    }
    g.number_players = 2
    g.current_player = 1
    g.date_started = datetime.now()
    mock_loadById.return_value = g
    service = turn.TurnService(GameModel, config)
    res = service.turn(
        game_id,
        1,
        play,
        dry_run=False
    )
    assert res == (False, turn.TurnService.INVALID_PLAY_CONTENT)


@patch.object(GameModel, "loadById")
@patch.object(GameModel, "save")
def test_turn_ok_next_player(mock_save, mock_loadById):
    game_id = '7fb8b876-a816-11e7-8b78-0469f8ed5e76'
    g = GameModel(config)
    g.id = game_id
    g.players = {
        1: {"id": 1, "name": "pierre", "hand": [10, 4, 5], "is_turn": True, "points": 0},
        2: {"id": 2, "name": "paul", "hand": [12, 13, 14], "is_turn": False, "points": 0}
    }
    g.number_players = 2
    g.current_player = 1
    g.date_started = datetime.now()
    mock_loadById.return_value = g
    service = turn.TurnService(GameModel, config)
    assert g.played_tokens == []
    assert g.players[1]["is_turn"] is True
    assert g.players[2]["is_turn"] is False
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
    assert mock_save.called
    assert g.played_tokens == [
            {'x': 7, 'y': 7, 'value': 10},
            {'x': 8, 'y': 7, 'value': 4}
    ]
    assert g.players[1]["is_turn"] is False
    assert g.players[2]["is_turn"] is True


@patch.object(GameModel, "loadById")
@patch.object(GameModel, "save")
def test_turn_dry_run(mock_save, mock_loadById):
    game_id = '7fb8b876-a816-11e7-8b78-0469f8ed5e76'
    g = GameModel(config)
    g.id = game_id
    g.players = {
        1: {"id": 1, "name": "pierre", "hand": [10, 4, 5], "is_turn": True, "points": 0},
        2: {"id": 2, "name": "paul", "hand": [12, 13, 14], "is_turn": False, "points": 0}
    }
    g.number_players = 2
    g.current_player = 1
    g.date_started = datetime.now()
    mock_loadById.return_value = g
    service = turn.TurnService(GameModel, config)
    assert g.played_tokens == []
    assert g.players[1]["is_turn"] is True
    assert g.players[2]["is_turn"] is False
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
    assert not mock_save.called
    assert g.played_tokens == []
    assert g.players[1]["is_turn"] is True
    assert g.players[1]["hand"] == [10, 4, 5]
    assert g.players[2]["is_turn"] is False


@patch.object(bag.Bag, 'is_empty')
@patch.object(bag.Bag, 'fill_hand')
@patch.object(GameModel, "loadById")
@patch.object(GameModel, "save")
def test_turn_ok_end_game(mock_save, mock_loadById, mock_fillHand, mock_isEmpty):
    mock_isEmpty.return_value = True
    mock_fillHand.return_value = []
    game_id = '7fb8b876-a816-11e7-8b78-0469f8ed5e76'
    g = GameModel(config)
    g.id = game_id
    g.players = {
        1: {"id": 1, "name": "pierre", "hand": [10, 4, 5], "is_turn": True, "points": 0},
        2: {"id": 2, "name": "paul", "hand": [7, 8, 4], "is_turn": False, "points": 0}
    }
    g.number_players = 2
    g.current_player = 1
    g.date_started = datetime.now()
    mock_loadById.return_value = g
    # should return all the plays for the whole bag, minus the current play,
    # which in then emptying the bag
    service = turn.TurnService(GameModel, config)
    assert g.date_finished is None
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
    assert mock_save.called
    assert g.date_finished is not None
    # Sum of the player's turns (1 in this case) + the other players' tokens
    assert g.players[1]["points"] == 24 + (7+8+4)
    assert g.players[2]["points"] == 0


@patch.object(GameModel, "loadById")
def test_turn_ko(mock_loadById):
    game_id = '7fb8b876-a816-11e7-8b78-0469f8ed5e76'
    g = GameModel(config)
    g.id = game_id
    g.players = {
        1: {"id": 1, "name": "pierre", "hand": [10, 4, 5], "is_turn": True, "points": 0},
        2: {"id": 2, "name": "paul", "hand": [7, 8, 4], "is_turn": False, "points": 0}
    }
    g.number_players = 2
    g.current_player = 1
    g.date_started = datetime.now()
    mock_loadById.return_value = g
    service = turn.TurnService(GameModel, config)
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


@patch.object(GameModel, "loadById")
def test_turn_unexisting_game(mock_loadById):
    mock_loadById.return_value = None
    service = turn.TurnService(GameModel, config)
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


@patch.object(GameModel, "loadById")
def test_turn_not_started_game(mock_loadById):
    game_id = '7fb8b876-a816-11e7-8b78-0469f8ed5e76'
    g = GameModel(config)
    g.id = game_id
    g.players = {
        1: {"id": 1, "name": "pierre", "hand": [10, 4, 5], "is_turn": True, "points": 0},
        2: {"id": 2, "name": "paul", "hand": [7, 8, 4], "is_turn": False, "points": 0}
    }
    g.number_players = 2
    g.current_player = 1
    mock_loadById.return_value = g
    service = turn.TurnService(GameModel, config)
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


@patch.object(GameModel, "loadById")
def test_turn_game_already_finished(mock_loadById):
    game_id = '7fb8b876-a816-11e7-8b78-0469f8ed5e76'
    g = GameModel(config)
    g.id = game_id
    g.players = {
        1: {"id": 1, "name": "pierre", "hand": [10, 4, 5], "is_turn": True, "points": 0},
        2: {"id": 2, "name": "paul", "hand": [7, 8, 4], "is_turn": False, "points": 0}
    }
    g.number_players = 2
    g.current_player = 1
    g.date_started = datetime.now()
    g.date_finished = datetime.now()
    mock_loadById.return_value = g
    service = turn.TurnService(GameModel, config)
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


@patch.object(GameModel, "loadById")
def test_turn_get_game_content_unknown_game(mock_loadById):
    mock_loadById.return_value = None
    service = turn.TurnService(GameModel, config)
    res = service.get_game_content('123')
    assert res is None


@patch.object(random, 'choice')
@patch.object(GameModel, "loadById")
@patch.object(GameModel, "save")
def test_turn_get_game_content(mock_save, mock_loadById, mock_choice):
    mock_choice.side_effect = [
        # hand refil player 1
        1,
        # hand refil player 2
        2, 3
    ]
    game_id = '7fb8b876-a816-11e7-8b78-0469f8ed5e76'
    g = GameModel(config)
    g.id = game_id
    g.players = {
        1: {"id": 1, "name": "pierre", "hand": [10, 4, 3], "is_turn": True, "points": 0},
        2: {"id": 2, "name": "paul", "hand": [10, 8, 7], "is_turn": False, "points": 0}
    }
    g.number_players = 2
    g.current_player = 1
    g.date_started = datetime.now()
    mock_loadById.return_value = g
    service = turn.TurnService(GameModel, config)
    res = service.turn(game_id, 1, [{'x':7,'y':7,'value':3}], dry_run=False)
    assert res[0] is True
    assert g.players[1]["hand"] == [10, 4, 1]
    res = service.turn(game_id, 2, [{'x':7,'y':8,'value':8}, {'x':8,'y':8,'value':7}], dry_run=False)
    assert res[0] is True
    assert g.players[2]["hand"] == [10, 2, 3]
    played_tokens, size_bag = service.get_game_content(game_id)
    expected_tokens = [
        {'x': 7, 'y': 7, 'value': 3},
        {'x': 7, 'y': 8, 'value': 8},
        {'x': 8, 'y': 8, 'value': 7}
    ]
    assert size_bag == 72
    assert played_tokens == expected_tokens
    assert mock_save.called


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
@patch.object(GameModel, "loadById")
@patch.object(GameModel, "save")
def test_skip_turn(mock_save, mock_loadById, player_hand, token_to_exchange, expected_result, dry_run):
    game_id = '7fb8b876-a816-11e7-8b78-0469f8ed5e76'
    g = GameModel(config)
    g.id = game_id
    g.players = {
        1: {"id": 1, "name": "pierre", "hand": player_hand, "is_turn": True, "points": 0},
        2: {"id": 2, "name": "paul", "hand": [10, 8, 7], "is_turn": False, "points": 0}
    }
    g.number_players = 2
    g.current_player = 1
    g.date_started = datetime.now()
    g.played_tokens = [
        {"x": 7, "y": 7, "value": 12},
        {"x": 8, "y": 7, "value": 3},
        {"x": 7, "y": 8, "value": 1},
        {"x": 8, "y": 8, "value": 9}
    ]
    mock_loadById.return_value = g
    service = turn.TurnService(GameModel, config)
    res = service.skip_turn(game_id, 1, token_to_exchange, dry_run=dry_run)
    assert res == expected_result
    if res[0]:
        if dry_run:
            assert g.players[1]["hand"] == player_hand
        else:
            assert token_to_exchange not in g.players[1]["hand"]
    assert mock_save.called == (res[0] and not dry_run)


@patch.object(bag.Bag, 'is_empty')
@patch.object(bag.Bag, 'fill_hand')
@patch.object(GameModel, "loadById")
@patch.object(GameModel, "save")
def test_skip_ok_end_game(mock_save, mock_loadById, mock_fillHand, mock_isEmpty):
    mock_isEmpty.return_value = True
    mock_fillHand.return_value = []
    game_id = '7fb8b876-a816-11e7-8b78-0469f8ed5e76'
    g = GameModel(config)
    g.id = game_id
    g.players = {
        1: {"id": 1, "name": "pierre", "hand": [12, 15, 14], "is_turn": True, "points": 0},
        2: {"id": 2, "name": "paul", "hand": [10, 8, 7], "is_turn": False, "points": 0}
    }
    g.number_players = 2
    g.current_player = 1
    g.date_started = datetime.now()
    g.played_tokens = [
        {"x": 7, "y": 7, "value": 12},
        {"x": 8, "y": 7, "value": 3},
        {"x": 7, "y": 8, "value": 1},
        {"x": 8, "y": 8, "value": 9}
    ]
    mock_loadById.return_value = g
    # should return all the plays for the whole bag, minus the current play,
    # which in then emptying the bag
    service = turn.TurnService(GameModel, config)
    res = service.skip_turn(
        game_id,
        1,
        15,
        dry_run=False
    )
    assert res == (True, {})
    # The hand should be unchanged
    assert g.players[1]["hand"] == [12, 15, 14]
    assert mock_save.called
