import requests
from unittest.mock import patch
from app.service.proxy import ProxyService
from tests.response import ResponseMock


def test_unknown_service():
    config = {
        'APP_NAME': 'api',
        'SERVICES': {
            'bar': {'base': 'http://localhost'}
        }
    }
    service = ProxyService(config)
    res = service.proxy(False, 'foo', '/foo/bar')
    assert not res[0]
    assert res[1] == ProxyService.UNKNOWN_SERVICE


def test_unknown_method():
    config = {
        'APP_NAME': 'api',
        'SERVICES': {
            'foo': {'base': 'http://localhost', 'need_auth': False}
        }
    }
    service = ProxyService(config)
    res = service.proxy(False, 'foo', '/foo/bar', method='TOTO')
    assert not res[0]
    assert res[1] == ProxyService.UNKNOWN_METHOD


@patch.object(requests, 'get')
def test_unknown_error(mock_get):
    mock_get.side_effect = requests.exceptions.RequestException()
    config = {
        'APP_NAME': 'api',
        'SERVICES': {
            'foo': {'base': 'http://localhost', 'need_auth': False}
        }
    }
    service = ProxyService(config)
    res = service.proxy(False, 'foo', '/foo/bar', method='GET')
    assert mock_get.called
    assert not res[0]
    assert res[1] == ProxyService.UNKNOWN_ERROR


@patch.object(requests, 'get')
def test_proxy_response(mock_get):
    response = ResponseMock(200)
    mock_get.return_value = response
    config = {
        'APP_NAME': 'api',
        'SERVICES': {
            'foo': {'base': 'http://localhost', 'need_auth': False}
        }
    }
    service = ProxyService(config)
    res = service.proxy(False, 'foo', '/foo/bar', method='GET')
    assert mock_get.called
    assert res[0]
    assert res[1] == response


def test_service_needs_auth_mismatch():
    config = {
        'APP_NAME': 'api',
        'SERVICES': {
            'foo': {'base': 'http://localhost', 'need_auth': False},
            'bar': {'base': 'http://localhost', 'need_auth': True}
        }
    }
    service = ProxyService(config)
    res1 = service.proxy(True, 'foo', '/foo/bar', method='GET')
    assert not res1[0]
    assert res1[1] == ProxyService.UNKNOWN_SERVICE
    res2 = service.proxy(False, 'bar', '/foo/bar', method='GET')
    assert not res2[0]
    assert res2[1] == ProxyService.UNKNOWN_SERVICE


def test_service_needs_auth():
    config = {
        'APP_NAME': 'api',
        'SERVICES': {
            'foo': {'base': 'http://localhost', 'need_auth': True}
        }
    }
    service = ProxyService(config)
    res = service.proxy(True, 'foo', '/foo/bar', method='GET')
    assert not res[0]
    assert res[1] == ProxyService.NEED_AUTHENTICATION


@patch.object(requests, 'get')
def test_service_auth_ok(mock_get):
    response = ResponseMock(200)
    mock_get.return_value = response
    config = {
        'APP_NAME': 'api',
        'SECRET_KEY': 'secret',
        'SERVICES': {
            'foo': {'base': 'http://localhost', 'need_auth': True}
        }
    }
    service = ProxyService(config)
    token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyaWQiOjEyMzR9.cmCIDClK8ZKWs-eujGbxrK7u7uynFHRX9eMRdmmj5Lw'
    res = service.proxy(True,
                        'foo',
                        '/foo/bar',
                        method='GET',
                        headers={
                            'X-Token': token
                        })

    url = 'http://localhost/foo/bar'
    headers = {
        'X-User': '{"userid": 1234}',
        'Content-type': 'application/json'
    }

    mock_get.assert_called_with(url, data='{}', headers=headers, params={})
    assert res[0]
    assert res[1] == response
