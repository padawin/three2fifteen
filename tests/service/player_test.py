from unittest.mock import patch
import requests

from app.service.player import PlayerService

config = {
    'APP_NAME': 'api',
    'SERVICE_GAME_BASE': 'foo',
    'SERVICE_GAME_CREATE_PLAYER': 'bar',
    'SERVICE_SOCIAL_BASE': 'foo',
    'SERVICE_SOCIAL_CREATE_PLAYER': 'bar'
}


@patch.object(requests, 'post')
def test_create_player_ok(mock_post):
    response = requests.Response()
    response.status_code = 200
    mock_post.return_value = response
    service = PlayerService(config)
    res = service.create(1)
    assert mock_post.called
    assert res[0]
    assert res[1]['status'] == 200


@patch.object(requests, 'post')
def test_create_player_ko_ConnectionError(mock_post):
    mock_post.side_effect = requests.exceptions.ConnectionError()
    service = PlayerService(config)
    res = service.create(1)
    assert mock_post.called
    assert not res[0]
    assert 'error' in res[1]
    assert isinstance(res[1]['error'], requests.exceptions.ConnectionError)


@patch.object(requests, 'post')
def test_create_player_ko_HTTPError(mock_post):
    mock_post.side_effect = requests.exceptions.HTTPError()
    service = PlayerService(config)
    res = service.create(1)
    assert mock_post.called
    assert not res[0]
    assert 'error' in res[1]
    assert isinstance(res[1]['error'], requests.exceptions.HTTPError)


@patch.object(requests, 'post')
def test_create_player_ko_Timeout(mock_post):
    mock_post.side_effect = requests.exceptions.Timeout()
    service = PlayerService(config)
    res = service.create(1)
    assert mock_post.called
    assert not res[0]
    assert 'error' in res[1]
    assert isinstance(res[1]['error'], requests.exceptions.Timeout)


@patch.object(requests, 'post')
def test_create_player_ko_TooManyRedirects(mock_post):
    mock_post.side_effect = requests.exceptions.TooManyRedirects()
    service = PlayerService(config)
    res = service.create(1)
    assert mock_post.called
    assert not res[0]
    assert 'error' in res[1]
    assert isinstance(res[1]['error'], requests.exceptions.TooManyRedirects)


@patch.object(requests, 'post')
def test_response_non_200(mock_post):
    response = requests.Response()
    response.status_code = 404
    mock_post.return_value = response
    service = PlayerService(config)
    res = service.create(1)
    assert mock_post.called
    assert res[1]['status'] == 404
