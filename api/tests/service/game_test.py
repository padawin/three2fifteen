import pytest
import uuid
from unittest.mock import patch

from api.service import game
from api.model.game import GameModel, games


@patch.object(uuid, 'uuid1')
def test_create_game_ok(
    mock_uuid
):
    assert len(games) == 0
    game_id = '7fb8b876-a816-11e7-8b78-0469f8ed5e76'
    mock_uuid.return_value = game_id
    service = game.GameService(GameModel)
    res = service.create('123', 'somelogin42', 3)
    assert len(games) == 1
    assert games[game_id].id == game_id
    assert games[game_id].number_players == 3
    assert games[game_id].players["123"]["id"] == "123"
    assert games[game_id].players["123"]["name"] == "somelogin42"
    assert games[game_id].current_player is None
    assert games[game_id].played_tokens == []
    assert res == (True, game_id)


def test_create_game_too_low_number_players():
    service = game.GameService(GameModel)
    res = service.create('123', 'johndoe', 1)
    assert not res[0]
    assert res[1] == game.GameService.INVALID_NUMBER_PLAYERS


def test_create_game_invalid_players_number_not_int():
    service = game.GameService(GameModel)
    res = service.create('123', 'johndoe', 'aha')
    assert not res[0]
    assert res[1] == game.GameService.INVALID_NUMBER_PLAYERS


def test_create_game_too_high_number_players():
    service = game.GameService(GameModel)
    res = service.create('123', 'johndoe', 5)
    assert not res[0]
    assert res[1] == game.GameService.INVALID_NUMBER_PLAYERS


@pytest.mark.parametrize(
    "size_game, players, result, code",
    [
        [
            4,
            [{"id": 1, "name": "pierre"}],
            True, None
        ],
        [
            4,
            [
                {"id": 1, "name": "pierre"},
                {"id": 2, "name": "paul"}
            ],
            True, None
        ],
        [
            3,
            [
                {"id": 1, "name": "pierre"},
                {"id": 2, "name": "paul"},
                {"id": 3, "name": "jack"}
            ],
            False, game.GameService.GAME_FULL
        ],
        [
            2,
            [
                {"id": 1, "name": "pierre"},
                {"id": 2, "name": "paul"}
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
def test_add_player_game(
    size_game,
    players,
    result,
    code
):
    service = game.GameService(GameModel)
    _, game_id = service.create(players[0]["id"], players[0]["name"], size_game)
    for player in players[1:]:
        service.add_player(game_id, player["id"], player["name"])
    res = service.add_player(game_id, 4, "hal")
    assert res[0] == result
    assert res[1] == code


def test_add_player_twice():
    service = game.GameService(GameModel)
    _, game_id = service.create(1, "john", 2)
    res = service.add_player(game_id, 1, "john")
    assert res[0] is False
    assert res[1] == game.GameService.PLAYER_ALREADY_IN_GAME


def test_add_player_with_same_name_as_other_player():
    service = game.GameService(GameModel)
    _, game_id = service.create(1, "john", 2)
    res = service.add_player(game_id, 2, "john")
    assert res[0] is False
    assert res[1] == game.GameService.PLAYER_NAME_ALREADY_IN_GAME


def test_add_player_no_game_found():
    service = game.GameService(GameModel)
    res = service.add_player('123', 'john', 1)
    assert res == (False, game.GameService.NO_GAME_FOUND)


def test_get_hand_no_game_found():
    service = game.GameService(GameModel)
    _, game_id = service.create(1, "john", 2)
    service.add_player(game_id, 2, "doe")
    res = service.get_player_hand('1331', 1)
    assert not res[0]
    assert res[1] == game.GameService.NO_GAME_FOUND


def test_get_hand_no_player_found():
    service = game.GameService(GameModel)
    _, game_id = service.create(1, "john", 2)
    service.add_player(game_id, 2, "doe")
    res = service.get_player_hand(game_id, 4)
    assert not res[0]
    assert res[1] == game.GameService.UNKNOWN_PLAYER


def test_get_hand():
    service = game.GameService(GameModel)
    _, game_id = service.create(1, "john", 2)
    service.add_player(game_id, 2, "doe")
    res = service.get_player_hand(game_id, 2)
    assert res[0] is True
    assert len(res[1]) == 3
