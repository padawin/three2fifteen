import pytest
from unittest.mock import patch

from app.model.model import DuplicateFieldError, Model
from app.model.player import PlayerModel
from app.service.user import UserService

from werkzeug.security import generate_password_hash


@patch.object(PlayerModel, 'insert')
def test_create_player_ok(mock_playerInsert):
    config = {'APP_NAME': 'foo'}
    mock_playerInsert.return_value = 1
    service = UserService(PlayerModel, config)
    res = service.create('username', 'password')
    assert mock_playerInsert.called
    assert res == (True, 1)


@patch.object(PlayerModel, 'insert')
def test_create_player_username_too_short(mock_playerInsert):
    config = {'APP_NAME': 'foo'}
    mock_playerInsert.return_value = 1
    service = UserService(PlayerModel, config)
    res = service.create('', 'password')
    assert not mock_playerInsert.called
    assert res == (False, UserService.USERNAME_TOO_SHORT)


@patch.object(PlayerModel, 'insert')
def test_create_player_trim_username(mock_playerInsert):
    config = {'APP_NAME': 'foo'}
    mock_playerInsert.return_value = 1
    service = UserService(PlayerModel, config)
    res = service.create('  ', 'password')
    assert not mock_playerInsert.called
    assert res == (False, UserService.USERNAME_TOO_SHORT)


@patch.object(PlayerModel, 'insert')
def test_create_player_trim_password(mock_playerInsert):
    config = {'APP_NAME': 'foo'}
    mock_playerInsert.return_value = 1
    service = UserService(PlayerModel, config)
    res = service.create('username', '1234      ')
    assert not mock_playerInsert.called
    assert res == (False, UserService.PASSWORD_TOO_SHORT)


@patch.object(PlayerModel, 'insert')
def test_create_login_too_long(mock_playerInsert):
    config = {'APP_NAME': 'foo'}
    service = UserService(PlayerModel, config)
    res = service.create(
        'usernameveryveryveryveryveryveryveryverylong',
        'password'
    )
    assert res == (False, UserService.USERNAME_TOO_LONG)
    assert not mock_playerInsert.called


def test_create_password_too_short():
    config = {'APP_NAME': 'foo'}
    service = UserService(PlayerModel, config)
    res = service.create(
        'username',
        'passwor'
    )
    assert res == (False, UserService.PASSWORD_TOO_SHORT)


@patch.object(PlayerModel, 'insert')
def test_create_player_duplicate(mock_playerInsert):
    config = {'APP_NAME': 'foo'}
    mock_playerInsert.side_effect = DuplicateFieldError()
    service = UserService(PlayerModel, config)
    res = service.create('username', 'password')
    assert mock_playerInsert.called
    assert res == (False, UserService.USERNAME_ALREADY_USED)


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
            UserService.INVALID_PASSWORD
        ],
        [
            [],
            'password',
            False,
            UserService.INVALID_USERNAME
        ],
        [
            [],
            'bar',
            False,
            UserService.INVALID_USERNAME
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
    config = {'APP_NAME': 'foo'}
    mock_loadBy.return_value = loadBy_result
    service = UserService(PlayerModel, config)
    res = service.get('foo', password)
    assert res[0] == expected_result
    if not res[0]:
        assert res[1] == reason
