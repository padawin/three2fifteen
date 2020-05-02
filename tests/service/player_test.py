from unittest.mock import patch
from werkzeug.security import generate_password_hash
import pytest

from app.model.model import DuplicateFieldError
from app.model.player import PlayerModel
from app.service import player
from app.service.player import PlayerService


@patch.object(PlayerModel, 'insert')
def test_create_player_ok(mock_playerInsert):
    mock_playerInsert.return_value = 1
    service = player.PlayerService(PlayerModel)
    res = service.create('username', 'password', 'foo')
    assert mock_playerInsert.called
    assert res == (True, 1)


@patch.object(PlayerModel, 'insert')
def test_create_player_username_too_short(mock_playerInsert):
    mock_playerInsert.return_value = 1
    service = PlayerService(PlayerModel)
    res = service.create('', 'password', 'foo')
    assert not mock_playerInsert.called
    assert res == (False, PlayerService.USERNAME_TOO_SHORT)


@patch.object(PlayerModel, 'insert')
def test_create_player_trim_username(mock_playerInsert):
    mock_playerInsert.return_value = 1
    service = PlayerService(PlayerModel)
    res = service.create('  ', 'password', 'foo')
    assert not mock_playerInsert.called
    assert res == (False, PlayerService.USERNAME_TOO_SHORT)


@patch.object(PlayerModel, 'insert')
def test_create_player_trim_password(mock_playerInsert):
    mock_playerInsert.return_value = 1
    service = PlayerService(PlayerModel)
    res = service.create('username', '1234      ', 'foo')
    assert not mock_playerInsert.called
    assert res == (False, PlayerService.PASSWORD_TOO_SHORT)


@patch.object(PlayerModel, 'insert')
def test_create_login_too_long(mock_playerInsert):
    service = PlayerService(PlayerModel)
    res = service.create(
        'usernameveryveryveryveryveryveryveryverylong',
        'password',
        'foo'
    )
    assert res == (False, PlayerService.USERNAME_TOO_LONG)
    assert not mock_playerInsert.called


def test_create_password_too_short():
    service = PlayerService(PlayerModel)
    res = service.create(
        'username',
        'passwor',
        'foo'
    )
    assert res == (False, PlayerService.PASSWORD_TOO_SHORT)


@patch.object(PlayerModel, 'insert')
def test_create_player_duplicate(mock_playerInsert):
    mock_playerInsert.side_effect = DuplicateFieldError()
    service = PlayerService(PlayerModel)
    res = service.create('username', 'password', 'foo')
    assert mock_playerInsert.called
    assert res == (False, PlayerService.USERNAME_ALREADY_USED)


@pytest.mark.parametrize(
    "loadBy_result, password, expected_result, reason",
    [
        [
            [{
                'username': 'foo',
                'password': generate_password_hash('password')
            }],
            'bar',
            False,
            PlayerService.INVALID_PASSWORD
        ],
        [
            [],
            'password',
            False,
            PlayerService.INVALID_USERNAME
        ],
        [
            [],
            'bar',
            False,
            PlayerService.INVALID_USERNAME
        ],
        [
            [{
                'username': 'foo',
                'password': generate_password_hash('password')
            }],
            'password',
            True,
            None
        ],
    ],
    # valids
    ids=["Wrong password",
         "Wrong username",
         "Wrong username and password",
         "Good username and password"]
)
@patch.object(PlayerModel, 'loadBy')
def test_check_password(mock_loadBy, loadBy_result, password, expected_result,
                        reason):
    mock_loadBy.return_value = loadBy_result
    service = PlayerService(PlayerModel)
    res = service.get('foo', password)
    assert res[0] == expected_result
    if not res[0]:
        assert res[1] == reason


def test_create_player_invalid_name():
    service = player.PlayerService(PlayerModel)
    res = service.create('username', 'password', '     ')
    assert res == (False, player.PlayerService.EMPTY_NAME)


def test_create_player_name_too_long():
    service = player.PlayerService(PlayerModel)
    res = service.create(
        'username',
        'password',
        ('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
         'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
    )
    assert res == (False, player.PlayerService.NAME_TOO_LONG)
