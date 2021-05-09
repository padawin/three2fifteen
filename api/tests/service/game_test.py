import pytest
from unittest.mock import patch

from api.service import game
from api.model.game import GameModel

config = {}


@patch.object(GameModel, "create")
@patch.object(GameModel, "add_player")
def test_create_game_ok(mock_addPlayer, mock_createGame):
    game_id = '7fb8b876-a816-11e7-8b78-0469f8ed5e76'
    g = GameModel(config)
    g.id = game_id
    mock_createGame.return_value = g
    service = game.GameService(GameModel, config)
    res = service.create('123', 'somelogin42', 3)
    assert mock_createGame.called
    assert mock_addPlayer.called
    assert res == (True, game_id)


def test_create_game_too_low_number_players():
    service = game.GameService(GameModel, config)
    res = service.create('123', 'johndoe', 1)
    assert not res[0]
    assert res[1] == game.GameService.INVALID_NUMBER_PLAYERS


def test_create_game_invalid_players_number_not_int():
    service = game.GameService(GameModel, config)
    res = service.create('123', 'johndoe', 'aha')
    assert not res[0]
    assert res[1] == game.GameService.INVALID_NUMBER_PLAYERS


def test_create_game_too_high_number_players():
    service = game.GameService(GameModel, config)
    res = service.create('123', 'johndoe', 5)
    assert not res[0]
    assert res[1] == game.GameService.INVALID_NUMBER_PLAYERS


@pytest.mark.parametrize(
    "size_game, players, new_player_id, new_player_name, result, code, start_game",
    [
        [
            4,
            {1: {"id": 1, "name": "pierre"}},
            4, "hal",
            True, None, False
        ],
        [
            2,
            {1: {"id": 1, "name": "pierre"}},
            4, "hal",
            True, None, True
        ],
        [
            4,
            {
                1: {"id": 1, "name": "pierre"},
                2: {"id": 2, "name": "paul"}
            },
            4, "hal",
            True, None, False
        ],
        [
            3,
            {
                1: {"id": 1, "name": "pierre"},
                2: {"id": 2, "name": "paul"},
                3: {"id": 3, "name": "jack"}
            },
            4, "hal",
            False, game.GameService.GAME_FULL, False
        ],
        [
            2,
            {
                1: {"id": 1, "name": "pierre"},
                2: {"id": 2, "name": "paul"}
            },
            4, "hal",
            False, game.GameService.GAME_FULL, False
        ],
        [
            3,
            {
                1: {"id": 1, "name": "pierre"},
                2: {"id": 2, "name": "paul"}
            },
            2, "paul",
            False, game.GameService.PLAYER_ALREADY_IN_GAME, False
        ],
        [
            3,
            {
                1: {"id": 1, "name": "pierre"},
                2: {"id": 2, "name": "paul"}
            },
            3, "paul",
            False, game.GameService.PLAYER_NAME_ALREADY_IN_GAME, False
        ]
    ],
    # valids
    ids=[
        "Add player 1",
        "Add player 2 start game",
        "Add player 2",
        "Add player 3",
        "Add player full game less than 4",
        "Add player already in game",
        "Add player name already in game"
    ]
)
@patch.object(GameModel, "loadById")
@patch.object(GameModel, "save")
@patch.object(GameModel, "start")
def test_add_player_game(
    mock_start,
    mock_save,
    mock_loadById,
    size_game,
    players,
    new_player_id,
    new_player_name,
    result,
    code,
    start_game
):
    game_id = '7fb8b876-a816-11e7-8b78-0469f8ed5e76'
    g = GameModel(config)
    g.id = game_id
    g.players = players
    g.number_players = size_game
    mock_loadById.return_value = g
    service = game.GameService(GameModel, config)
    res = service.add_player(game_id, new_player_id, new_player_name)
    assert res[0] == result
    assert res[1] == code
    assert mock_start.called == start_game


@patch.object(GameModel, "loadById")
def test_add_player_no_game_found(mock_loadById):
    mock_loadById.return_value = None
    service = game.GameService(GameModel, config)
    res = service.add_player('123', 'john', 1)
    assert res == (False, game.GameService.NO_GAME_FOUND)


@patch.object(GameModel, "loadById")
def test_get_hand_no_game_found(mock_loadById):
    mock_loadById.return_value = None
    service = game.GameService(GameModel, config)
    res = service.get_player_hand('1331', 1)
    assert not res[0]
    assert res[1] == game.GameService.NO_GAME_FOUND


@patch.object(GameModel, "loadById")
def test_get_hand_no_player_found(mock_loadById):
    game_id = '7fb8b876-a816-11e7-8b78-0469f8ed5e76'
    g = GameModel(config)
    g.id = game_id
    g.players = {
        1: {"id": 1, "name": "pierre"},
        2: {"id": 2, "name": "paul"}
    }
    mock_loadById.return_value = g
    service = game.GameService(GameModel, config)
    res = service.get_player_hand(game_id, 4)
    assert not res[0]
    assert res[1] == game.GameService.UNKNOWN_PLAYER


@patch.object(GameModel, "loadById")
def test_get_hand(mock_loadById):
    game_id = '7fb8b876-a816-11e7-8b78-0469f8ed5e76'
    g = GameModel(config)
    g.id = game_id
    g.players = {
        1: {"id": 1, "name": "pierre", "hand": [1, 2, 3]},
        2: {"id": 2, "name": "paul", "hand": [12, 13, 14]}
    }
    mock_loadById.return_value = g
    service = game.GameService(GameModel, config)
    res = service.get_player_hand(game_id, 2)
    assert res[0] is True
    assert res[1] == [12, 13, 14]
