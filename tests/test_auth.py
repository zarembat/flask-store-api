from tests.conftest import TestResponse


def test_get_token(client, auth_user):
    response: TestResponse = client.post(
        '/auth',
        content_type='application/json',
        json={
            'username': auth_user.username,
            'password': auth_user.password
        }
    )
    assert "access_token" in response.json
    assert response.status_code == 200


def test_get_token_invalid_credentials(client, auth_user):
    response: TestResponse = client.post(
        '/auth',
        content_type='application/json',
        json={
            'username': 'wrong',
            'password': 'wrong'
        }
    )
    assert b"Invalid credentials" in response.data
    assert response.status_code == 401


def test_endpoint_jwt_required_no_token(client):
    response: TestResponse = client.post(
        '/store/test_store',
        content_type='application/json'
    )
    assert response.status_code == 500


def test_endpoint_jwt_required(client, auth_user, auth_user_tokens):
    response: TestResponse = client.post(
        '/store/test_store',
        content_type='application/json',
        headers={
            'Authorization': 'Bearer ' + auth_user_tokens['access_token']
        }
    )
    assert "id" in response.json
    assert response.status_code == 201


def test_admin_privilege_required(client, admin_user_tokens):
    response: TestResponse = client.delete(
        '/store/test_store',
        content_type='application/json',
        headers={
            'Authorization': 'Bearer ' + admin_user_tokens['access_token']
        }
    )
    assert b"deleted" in response.data
    assert response.status_code == 200


def test_admin_privilege_required_no_admin(client, auth_user_tokens):
    response: TestResponse = client.delete(
        '/store/test_store',
        content_type='application/json',
        headers={
            'Authorization': 'Bearer ' + auth_user_tokens['access_token']
        }
    )
    assert b"privilege" in response.data
    assert response.status_code == 401


def test_optional_token(item, client, auth_user_tokens):
    response: TestResponse = client.get(
        '/items',
        content_type='application/json',
        headers={
            'Authorization': 'Bearer ' + auth_user_tokens['access_token']
        }
    )
    assert b"message" not in response.data
    assert response.status_code == 200


def test_optional_token_no_token(item, client, auth_user_tokens):
    response: TestResponse = client.get(
        '/items',
        content_type='application/json'
    )
    assert b"message" in response.data
    assert response.status_code == 200


def test_token_refresh_wrong_token(client, auth_user_tokens):
    response: TestResponse = client.post(
        '/refresh',
        content_type='application/json',
        headers={
            'Authorization': 'Bearer ' + auth_user_tokens['access_token']
        }
    )
    assert response.status_code == 500


def test_token_refresh(client, auth_user_tokens):
    response: TestResponse = client.post(
        '/refresh',
        content_type='application/json',
        headers={
            'Authorization': 'Bearer ' + auth_user_tokens['refresh_token']
        }
    )
    assert "access_token" in response.json
    assert response.status_code == 200
