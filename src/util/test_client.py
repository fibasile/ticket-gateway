import pytest
from flask_jwt_extended import create_access_token


@pytest.fixture(scope='session')
def test_client(flask_app):
    with flask_app.app_context():
        token = create_access_token(identity='testclient')
        client = flask_app.test_client()
        client.environ_base['HTTP_AUTHORIZATION'] = 'Bearer ' + token
        return client
