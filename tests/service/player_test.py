from unittest.mock import patch
import requests

from app.service import player
from app.service.player import PlayerService
from app.model.model import DuplicateFieldError, InvalidDataError, Model
from app.model.player import PlayerModel

config = {
    'APP_NAME': 'api',
    'SERVICE_GAME_BASE': 'foo',
    'SERVICE_GAME_CREATE_PLAYER': 'bar',
    'SERVICE_SOCIAL_BASE': 'foo',
    'SERVICE_SOCIAL_CREATE_PLAYER': 'bar'
}


@patch.object(PlayerModel, 'insert')
@patch.object(Model, 'commit')
def test_create_player_ok(mock_commit, mock_playerInsert):
    mock_playerInsert.return_value = 1
    service = player.PlayerService(PlayerModel)
    res = service.create(3, 'foo')
    mock_playerInsert.assert_called_with({'id_user': 3, 'name': 'foo'})
    assert res == (True, 1)
    assert mock_commit.called


@patch.object(PlayerModel, 'insert')
@patch.object(Model, 'rollback')
def test_create_player_duplicate(mock_rollback, mock_playerInsert):
    mock_playerInsert.side_effect = DuplicateFieldError()
    service = player.PlayerService(PlayerModel)
    res = service.create(3, 'foo')
    mock_playerInsert.assert_called_with({'id_user': 3, 'name': 'foo'})
    assert res == (False, player.PlayerService.USER_ID_ALREADY_USED)
    assert mock_rollback.called


@patch.object(PlayerModel, 'insert')
@patch.object(Model, 'rollback')
def test_create_player_invalid_id(mock_rollback, mock_playerInsert):
    mock_playerInsert.side_effect = InvalidDataError()
    service = player.PlayerService(PlayerModel)
    res = service.create(3, 'foo')
    mock_playerInsert.assert_called_with({'id_user': 3, 'name': 'foo'})
    assert res == (False, player.PlayerService.INVALID_USER_ID)
    assert mock_rollback.called


def test_create_player_invalid_name():
    service = player.PlayerService(PlayerModel)
    res = service.create(3, '   ')
    assert res == (False, player.PlayerService.EMPTY_NAME)


def test_create_player_name_too_long():
    service = player.PlayerService(PlayerModel)
    res = service.create(
        3,
        ('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
         'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
    )
    assert res == (False, player.PlayerService.NAME_TOO_LONG)
