import pytest
from unittest.mock import patch

from app.game import bag
from app.service import turn
from app.model.model import Model
from app.model.turn import TurnModel
from app.model.game import GameModel
from app.model.game_player import GamePlayerModel


@patch.object(GamePlayerModel, 'fetchAllRows')
@patch.object(GameModel, 'loadById')
def test_invalid_play_type(mock_gameLoadById, mock_getCurrentPlayerFetchAllRows):
    mock_getCurrentPlayerFetchAllRows.return_value = [{
        'id_player': '456',
        'hand': [10, 4, 5]
    }]
    mock_gameLoadById.return_value = {
        'date_started': 'some date',
        'date_finished': None
    }
    service = turn.TurnService(GameModel, TurnModel, GamePlayerModel)
    fixtures = (
        ({'x': 8, 'y': 7, 'value': 4}, turn.TurnService.INVALID_PLAY_TOKEN),
        ({'x': 8, 'toto': 7, 'value': 4}, turn.TurnService.INVALID_PLAY_TYPE),
        ({'x': 8, 'toto': 7, 'value': 4}, turn.TurnService.INVALID_PLAY_TYPE),
    )
    for play, result in fixtures:
        res = service.turn('123', '456', [play, 'foo'], dry_run=False)
        assert res == (False, result)


@patch.object(GamePlayerModel, 'fetchAllRows')
@patch.object(GameModel, 'loadById')
def test_wrong_turn_player(mock_gameLoadById, mock_getCurrentPlayerFetchAllRows):
    mock_gameLoadById.return_value = {
        'date_started': 'some date',
        'date_finished': None
    }
    mock_getCurrentPlayerFetchAllRows.return_value = [{
        'id_player': '456',
        'hand': [10, 4, 5]
    }]
    service = turn.TurnService(GameModel, TurnModel, GamePlayerModel)
    res = service.turn(
        '123',
        '789',
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
@patch.object(GamePlayerModel, 'fetchAllRows')
@patch.object(GameModel, 'loadById')
def test_play_not_in_hand(mock_gameLoadById, mock_getCurrentPlayerFetchAllRows, hand, play):
    mock_gameLoadById.return_value = {
        'date_started': 'some date',
        'date_finished': None
    }
    mock_getCurrentPlayerFetchAllRows.return_value = [
        {'id_player': '456', 'hand': hand}
    ]
    service = turn.TurnService(GameModel, TurnModel, GamePlayerModel)
    res = service.turn(
        '123',
        '456',
        play,
        dry_run=False
    )
    assert res == (False, turn.TurnService.INVALID_PLAY_CONTENT)


@patch.object(TurnModel, 'fetchAllRows')
@patch.object(TurnModel, 'insert')
@patch.object(GameModel, 'loadById')
@patch.object(GamePlayerModel, 'set_points_and_hand')
@patch.object(GamePlayerModel, 'fetchAllRows')
@patch.object(GamePlayerModel, 'next_player')
@patch.object(Model, 'commit')
def test_turn_ok_next_player(
    mock_commit,
    mock_nextPlayer,
    mock_getPlayersfetchAllRows,
    mock_set_points_and_hand,
    mock_gameLoadById,
    mock_insert,
    mock_turnFetchAllRows
):
    mock_getPlayersfetchAllRows.return_value = [
        {
            'id_game_player': 12,
            'id_user': 2,
            'id_player': 2,
            'is_turn': True,
            'hand': [10, 4, 5]
        },
        {
            'id_game_player': 10,
            'id_user': 1,
            'id_player': 1,
            'is_turn': False,
            'hand': [10, 4, 5]
        },
        {
            'id_game_player': 11,
            'id_user': 3,
            'id_player': 3,
            'is_turn': False,
            'hand': [10, 4, 5]
        }
    ]
    mock_gameLoadById.return_value = {
        'date_started': 'some date',
        'date_finished': None
    }
    mock_turnFetchAllRows.return_value = []
    service = turn.TurnService(GameModel, TurnModel, GamePlayerModel)
    res = service.turn(
        1,
        2,
        [
            {'x': 7, 'y': 7, 'value': 10},
            {'x': 8, 'y': 7, 'value': 4}
        ],
        dry_run=False
    )
    assert mock_turnFetchAllRows.called
    mock_nextPlayer.assert_called_with(12, 10)
    mock_insert.assert_called_with({
        'id_game': 1,
        'id_player': 2,
        'x': [7, 8],
        'y': [7, 7],
        'value': [10, 4],
        'score': 24
    })
    assert mock_set_points_and_hand.called
    assert mock_commit.called
    assert res == (
        True,
        {
            'id_game': 1,
            'id_player': 2,
            'x': [7, 8],
            'y': [7, 7],
            'value': [10, 4],
            'score': 24
        }
    )


@patch.object(TurnModel, 'fetchAllRows')
@patch.object(TurnModel, 'insert')
@patch.object(GamePlayerModel, 'set_points_and_hand')
@patch.object(GamePlayerModel, 'fetchAllRows')
@patch.object(GameModel, 'loadById')
@patch.object(GameModel, '_update_date')
@patch.object(Model, 'commit')
@patch.object(bag.Bag, 'is_empty')
@patch.object(bag.Bag, 'fill_hand')
@patch.object(GamePlayerModel, 'next_player')
def test_turn_ok_end_game(
    mock_nextPlayer,
    mock_fillHand,
    mock_isEmpty,
    mock_commit,
    mock_updateDate,
    mock_gameLoadById,
    mock_getCurrentPlayerFetchAllRows,
    mock_set_points_and_hand,
    mock_insert,
    mock_turnFetchAllRows
):
    mock_isEmpty.return_value = True
    mock_fillHand.return_value = []
    mock_getCurrentPlayerFetchAllRows.return_value = [{
        'id_game_player': 12,
        'id_player': 2,
        'hand': [10, 4]
    }]
    mock_gameLoadById.return_value = {
        'date_started': 'some date',
        'date_finished': None
    }
    mock_turnFetchAllRows.return_value = []
    # should return all the plays for the whole bag, minus the current play,
    # which in then emptying the bag
    service = turn.TurnService(GameModel, TurnModel, GamePlayerModel)
    res = service.turn(
        1,
        2,
        [
            {'x': 7, 'y': 7, 'value': 10},
            {'x': 8, 'y': 7, 'value': 4}
        ],
        dry_run=False
    )
    assert mock_turnFetchAllRows.called
    mock_nextPlayer.assert_called_with(12)
    mock_insert.assert_called_with({
        'id_game': 1,
        'id_player': 2,
        'x': [7, 8],
        'y': [7, 7],
        'value': [10, 4],
        'score': 24
    })
    assert mock_set_points_and_hand.called
    assert mock_updateDate.called
    assert mock_commit.called
    assert res == (True, {
        'id_game': 1,
        'id_player': 2,
        'x': [7, 8],
        'y': [7, 7],
        'value': [10, 4],
        'score': 24
    })


@patch.object(TurnModel, 'fetchAllRows')
@patch.object(GameModel, 'loadById')
@patch.object(GamePlayerModel, 'fetchAllRows')
def test_turn_ko(mock_getCurrentPlayerFetchAllRows, mock_gameLoadById, mock_turnFetchAllRows):
    mock_getCurrentPlayerFetchAllRows.return_value = [{
        'id_player': '456',
        'hand': [10, 4, 5]
    }]
    mock_gameLoadById.return_value = {
        'date_started': 'some date',
        'date_finished': None
    }
    mock_turnFetchAllRows.return_value = []
    service = turn.TurnService(GameModel, TurnModel, GamePlayerModel)
    res = service.turn(
        '123',
        '456',
        [
            {'x': 5, 'y': 7, 'value': 10},
            {'x': 8, 'y': 8, 'value': 4}
        ],
        dry_run=False
    )
    assert mock_turnFetchAllRows.called
    assert res[0] is False


@patch.object(GameModel, 'loadById')
def test_turn_unexisting_game(mock_gameLoadById):
    mock_gameLoadById.return_value = None
    service = turn.TurnService(GameModel, TurnModel, GamePlayerModel)
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


@patch.object(GameModel, 'loadById')
def test_turn_not_started_game(mock_gameLoadById):
    mock_gameLoadById.return_value = {
        'date_started': None,
        'date_finished': None
    }
    service = turn.TurnService(GameModel, TurnModel, GamePlayerModel)
    res = service.turn(
        '123',
        '456',
        [
            {'x': 5, 'y': 7, 'value': 10},
            {'x': 8, 'y': 8, 'value': 4}
        ],
        dry_run=False
    )
    assert res == (False, turn.TurnService.GAME_NOT_STARTED)
    res = service.skip_turn('123', '456', 10, dry_run=False)
    assert res == (False, turn.TurnService.GAME_NOT_STARTED)


@patch.object(GameModel, 'loadById')
def test_turn_game_already_finished(mock_gameLoadById):
    mock_gameLoadById.return_value = {
        'date_started': 'some date',
        'date_finished': 'some other date'
    }
    service = turn.TurnService(GameModel, TurnModel, GamePlayerModel)
    res = service.turn(
        '123',
        '456',
        [
            {'x': 5, 'y': 7, 'value': 10},
            {'x': 8, 'y': 8, 'value': 4}
        ],
        dry_run=False
    )
    assert res == (False, turn.TurnService.GAME_FINISHED)
    res = service.skip_turn('123', '456', 10, dry_run=False)
    assert res == (False, turn.TurnService.GAME_FINISHED)


@patch.object(GameModel, 'loadById')
def test_turn_get_game_content_unknown_game(mock_gameLoadById):
    mock_gameLoadById.return_value = {}
    service = turn.TurnService(GameModel, TurnModel, GamePlayerModel)
    res = service.get_game_content(123)
    assert res is None


@patch.object(GameModel, 'loadById')
@patch.object(GamePlayerModel, 'fetchAllRows')
@patch.object(TurnModel, 'fetchAllRows')
def test_turn_get_game_content(mock_turnFetchAllRows, mock_getPlayersfetchAllRows, mock_gameLoadById):
    mock_gameLoadById.return_value = {'id_game': 123}
    mock_turnFetchAllRows.return_value = [
        {
            'x': [1],
            'y': [2],
            'value': [3],
            'id_user': 1,
            'id_player': 1,
            'score': 3
        },
        {
            'x': [4, 5],
            'y': [6, 7],
            'value': [8, 7],
            'id_user': 2,
            'id_player': 2,
            'score': 15
        }
    ]
    mock_getPlayersfetchAllRows.return_value = [
        {
            'id_game_player': 12,
            'id_user': 2,
            'id_player': 2,
            'is_turn': True,
            'hand': [0, 0, 0]
        },
        {
            'id_game_player': 10,
            'id_user': 1,
            'id_player': 1,
            'is_turn': False,
            'hand': [6, 0, 0]
        },
        {
            'id_game_player': 11,
            'id_user': 3,
            'id_player': 3,
            'is_turn': False,
            'hand': [15, 0, 0]
        }
    ]
    service = turn.TurnService(GameModel, TurnModel, GamePlayerModel)
    played_tokens, size_bag = service.get_game_content(123)
    expected_tokens = [
        {'x': 1, 'y': 2, 'value': 3},
        {'x': 4, 'y': 6, 'value': 8},
        {'x': 5, 'y': 7, 'value': 7}
    ]
    assert size_bag == 69
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
@patch.object(GameModel, 'loadById')
@patch.object(TurnModel, 'fetchAllRows')
@patch.object(GamePlayerModel, 'fetchAllRows')
@patch.object(GamePlayerModel, 'set_points_and_hand')
@patch.object(GamePlayerModel, 'next_player')
@patch.object(Model, 'commit')
def test_skip_turn(
    mock_commit, mock_nextPlayer, mock_set_points_and_hand, mock_getPlayersfetchAllRows, mock_turnFetchAllRows, mock_gameLoadById,
    player_hand, token_to_exchange, expected_result, dry_run
):
    mock_gameLoadById.return_value = {
        'date_started': 'some date',
        'date_finished': None
    }
    mock_turnFetchAllRows.return_value = [
        {
            'x': [7, 8],
            'y': [7, 7],
            'value': [12, 3],
            'id_user': 1,
            'id_player': 1,
            'score': 3
        },
        {
            'x': [7, 8],
            'y': [8, 8],
            'value': [1, 9],
            'id_user': 2,
            'id_player': 2,
            'score': 15
        }
    ]
    mock_getPlayersfetchAllRows.return_value = [
        {
            'id_game_player': 12,
            'id_user': 2,
            'id_player': 2,
            'is_turn': True,
            'hand': player_hand
        },
        {
            'id_game_player': 10,
            'id_user': 1,
            'id_player': 1,
            'is_turn': False,
            'hand': [10, 4, 5]
        },
        {
            'id_game_player': 11,
            'id_user': 3,
            'id_player': 3,
            'is_turn': False,
            'hand': [10, 4, 5]
        }
    ]
    service = turn.TurnService(GameModel, TurnModel, GamePlayerModel)
    res = service.skip_turn(123, 2, token_to_exchange, dry_run=dry_run)
    assert res == expected_result
    assert mock_commit.called is (res[0] and not dry_run)
    assert mock_nextPlayer.called is (res[0] and not dry_run)
    assert mock_set_points_and_hand.called is (res[0] and not dry_run)
