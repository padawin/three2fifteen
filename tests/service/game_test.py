import pytest
import uuid
from unittest.mock import patch

from app.service import game
from app.model.model import DuplicateFieldError, Model
from app.model.game import GameModel
from app.model.game_player import GamePlayerModel
from app.model.player import PlayerModel
from app.model.turn import TurnModel


@patch.object(GameModel, 'insert')
@patch.object(GamePlayerModel, 'insert')
@patch.object(PlayerModel, 'loadBy')
@patch.object(uuid, 'uuid1')
@patch.object(Model, 'commit')
def test_create_game_ok(
    mock_commit, mock_uuid, mock_playerLoadBy, mock_gamePlayerInsert, mock_gameInsert
):
    game_public_id = '7fb8b876-a816-11e7-8b78-0469f8ed5e76'
    mock_gameInsert.return_value = 1
    mock_playerLoadBy.return_value = [1]
    mock_uuid.return_value = game_public_id
    service = game.GameService(GameModel, GamePlayerModel, PlayerModel)
    res = service.create('123', 3)
    mock_gameInsert.assert_called_with({
        "number_players": 3,
        "public_id": game_public_id
    })
    mock_gamePlayerInsert.assert_called_with({
        "id_game": 1,
        "id_player": '123',
        "is_game_creator": True
    })
    assert mock_commit.called
    assert res == (True, 1)


@patch.object(GamePlayerModel, 'loadGamesFromPlayerId')
def test_getPlayerGames(mock_loadGamesFromPlayerId):
    service = game.GameService(GameModel, GamePlayerModel, PlayerModel)
    service.getPlayerGames(1)
    assert mock_loadGamesFromPlayerId.called


def test_create_game_too_low_number_players():
    service = game.GameService(GameModel, GamePlayerModel, PlayerModel)
    res = service.create('123', 1)
    assert not res[0]
    assert res[1] == game.GameService.INVALID_NUMBER_PLAYERS


def test_create_game_invalid_players_number_not_int():
    service = game.GameService(GameModel, GamePlayerModel, PlayerModel)
    res = service.create('123', 'aha')
    assert not res[0]
    assert res[1] == game.GameService.INVALID_NUMBER_PLAYERS


@patch.object(PlayerModel, 'loadBy')
@patch.object(Model, 'rollback')
def test_create_game_unknown_player(mock_rollback, mock_playerLoadBy):
    mock_playerLoadBy.return_value = []
    service = game.GameService(GameModel, GamePlayerModel, PlayerModel)
    res = service.create('123', 3)
    assert mock_playerLoadBy.called
    assert not res[0]
    assert res[1] == game.GameService.UNKNOWN_PLAYER


def test_create_game_too_high_number_players():
    service = game.GameService(GameModel, GamePlayerModel, PlayerModel)
    res = service.create('123', 5)
    assert not res[0]
    assert res[1] == game.GameService.INVALID_NUMBER_PLAYERS


@pytest.mark.parametrize(
    "size_game, players, result, code",
    [
        [
            4,
            [{"id_game": 1, "id_player": 1}],
            True, None
        ],
        [
            4,
            [{"id_game": 1, "id_player": 1}, {"id_game": 1, "id_player": 2}],
            True, None
        ],
        [
            3,
            [
                {"id_game": 1, "id_player": 1},
                {"id_game": 1, "id_player": 2},
                {"id_game": 1, "id_player": 3}
            ],
            False, game.GameService.GAME_FULL
        ],
        [
            2,
            [
                {"id_game": 1, "id_player": 1},
                {"id_game": 1, "id_player": 2}
            ],
            False, game.GameService.GAME_FULL
        ]
    ],
    # valids
    ids=["Add player 1",
         "Add player 2",
         "Add player 3",
         "Add player full game less than 4"]
)
@patch.object(GameModel, 'loadBy')
@patch.object(GamePlayerModel, 'loadBy')
@patch.object(GamePlayerModel, 'insert')
@patch.object(PlayerModel, 'loadBy')
@patch.object(Model, 'commit')
@patch.object(Model, 'rollback')
def test_add_player_game(
    mock_rollback,
    mock_commit,
    mock_playerLoadBy,
    mock_insert,
    mock_gamePlayerLoadBy,
    mock_gameLoadBy,
    size_game,
    players,
    result,
    code
):
    mock_gameLoadBy.return_value = [{"id_game": 123, "number_players": size_game}]
    mock_gamePlayerLoadBy.return_value = players
    mock_playerLoadBy.return_value = [1]
    service = game.GameService(GameModel, GamePlayerModel, PlayerModel)
    res = service.addPlayer(123, 1)
    assert res[0] == result
    if not result:
        assert mock_rollback.called
        assert res[1] == code
    else:
        assert mock_commit.called
        mock_insert.assert_called_with({
            "id_game": 123,
            "id_player": 1,
            "is_game_creator": False
        })


@patch.object(GameModel, 'update')
@patch.object(GameModel, 'loadBy')
@patch.object(PlayerModel, 'loadBy')
@patch.object(GamePlayerModel, 'set_hand')
@patch.object(GamePlayerModel, 'set_first_player')
@patch.object(GamePlayerModel, 'loadBy')
@patch.object(GamePlayerModel, 'insert')
@patch.object(Model, 'commit')
def test_add_last_player(
    mock_commit,
    mock_insert,
    mock_gamePlayerLoadBy,
    mock_set_first_player,
    mock_set_hand,
    mock_playerLoadBy,
    mock_gameLoadBy,
    mock_update
):
    mock_gameLoadBy.return_value = [{"id_game": 123, "number_players": 2}]
    mock_gamePlayerLoadBy.return_value = [{"id_game": 1, "id_player": 1}]
    mock_playerLoadBy.return_value = [1]
    service = game.GameService(GameModel, GamePlayerModel, PlayerModel)
    res = service.addPlayer(123, 1)
    assert res[0] is True
    assert mock_update.called
    assert mock_set_first_player.called
    assert mock_set_hand.called
    assert mock_commit.called
    mock_insert.assert_called_with({
        "id_game": 123,
        "id_player": 1,
        "is_game_creator": False
    })


@patch.object(GameModel, 'loadBy')
@patch.object(GamePlayerModel, 'loadBy')
@patch.object(GamePlayerModel, 'insert')
@patch.object(PlayerModel, 'loadBy')
@patch.object(Model, 'rollback')
def test_add_player_twice(mock_rollback, mock_playerLoadBy, mock_insert, mock_gamePlayerLoadBy, mock_gameLoadBy):
    mock_gameLoadBy.return_value = [{"id_game": 1, "number_players": 4}]
    mock_gamePlayerLoadBy.return_value = [
        {"id_game": 1, "id_player": 1},
        {"id_game": 1, "id_player": 1},
    ]
    mock_playerLoadBy.return_value = [1]
    mock_insert.side_effect = DuplicateFieldError()
    service = game.GameService(GameModel, GamePlayerModel, PlayerModel)
    res = service.addPlayer('123', 1)
    assert mock_rollback.called
    assert res[0] is False
    assert res[1] == game.GameService.PLAYER_ALREADY_IN_GAME


@patch.object(PlayerModel, 'loadBy')
@patch.object(GameModel, 'loadBy')
@patch.object(Model, 'rollback')
def test_add_player_unknown_player(mock_rollback, mock_gameLoadBy, mock_playerLoadBy):
    mock_playerLoadBy.return_value = []
    mock_gameLoadBy.return_value = [{"id_game": 1, "number_players": 4}]
    service = game.GameService(GameModel, GamePlayerModel, PlayerModel)
    res = service.addPlayer('123', 1)
    assert mock_rollback.called
    assert res == (False, game.GameService.UNKNOWN_PLAYER)


@patch.object(GameModel, 'loadBy')
@patch.object(Model, 'rollback')
def test_add_player_no_game_found(mock_rollback, mock_gameLoadBy):
    mock_gameLoadBy.return_value = []
    service = game.GameService(GameModel, GamePlayerModel, PlayerModel)
    res = service.addPlayer('123', 1)
    assert mock_rollback.called
    assert res == (False, game.GameService.NO_GAME_FOUND)


@patch.object(GamePlayerModel, 'loadBy')
def test_get_hand_no_game_found(mock_gamePlayerLoadBy):
    mock_gamePlayerLoadBy.return_value = []
    service = game.GameService(GameModel, GamePlayerModel, PlayerModel)
    res = service.get_player_hand('123', 1)
    assert not res


@patch.object(GamePlayerModel, 'loadBy')
def test_get_hand(mock_gamePlayerLoadBy):
    mock_gamePlayerLoadBy.return_value = [{'hand': [1, 2, 3]}]
    service = game.GameService(GameModel, GamePlayerModel, PlayerModel)
    res = service.get_player_hand('123', 1)
    assert res == [1, 2, 3]
