from tests import conftest


def test_user_register(client):
    response: conftest.TestResponse = client.post(
        '/register',
        content_type='application/json',
        json={
            'username': conftest.TEST_USER_USERNAME,
            'password': conftest.TEST_USER_PASSWORD
        }
    )
    assert b"successfully" in response.data
    assert response.status_code == 201


def test_user_already_exists(client, auth_user):
    response: conftest.TestResponse = client.post(
        '/register',
        content_type='application/json',
        json={
            'username': auth_user.username,
            'password': auth_user.password
        }
    )
    assert b"already exists" in response.data
    assert response.status_code == 400


def test_get_store_by_name(store, client, auth_user_tokens):
    response: conftest.TestResponse = client.get(
        f'/store/{store.name}',
        content_type='application/json',
        headers={
            'Authorization': 'Bearer ' + auth_user_tokens['access_token']
        }
    )
    assert store.name.encode() in response.data
    assert response.status_code == 200


def test_get_store_by_name_not_exist(client, auth_user_tokens):
    response: conftest.TestResponse = client.get(
        '/store/non_existent_store_name',
        content_type='application/json',
        headers={
            'Authorization': 'Bearer ' + auth_user_tokens['access_token']
        }
    )
    assert b"not found" in response.data
    assert response.status_code == 404
