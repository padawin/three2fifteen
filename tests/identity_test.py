from app.identity import Identity


def test_token_not_in_headers():
    token = Identity.get({}, {})
    assert token is None


def test_token_not_valid():
    token = Identity.get({'X-Token': 'foobar'}, {'SECRET_KEY': 'secret'})
    assert token is None
    token = Identity.get({'X-Token': 'foo.bar'}, {'SECRET_KEY': 'secret'})
    assert token is None


def test_ok():
    token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyaWQiOjEyMzR9.cmCIDClK8ZKWs-eujGbxrK7u7uynFHRX9eMRdmmj5Lw'
    decoded = Identity.get({'X-Token': token}, {'SECRET_KEY': 'secret'})
    assert decoded == {'userid': 1234}
