import os
import pytest

from flask import Flask
from werkzeug.test import TestResponse
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token
)

from app import create_app
from tests import constants
from db import db
from models.store import StoreModel
from models.item import ItemModel
from models.user import UserModel


# Prevent pytest from trying to collect TestResponse as tests:
TestResponse.__test__ = False

# Constants to be used in tests
TEST_STORE_NAME = "Testing store"
TEST_ITEM_NAME = "Item name"
TEST_ITEM_PRICE = 99.99
TEST_ITEM_STORE_ID = 1
TEST_USER_USERNAME = "test_user"
TEST_USER_PASSWORD = "test_user_password"
TEST_AUTH_USER_USERNAME = "auth_user"
TEST_AUTH_USER_PASSWORD = "auth_user_password"
TEST_AUTH_ADMIN_USERNAME = "admin_user"
TEST_AUTH_ADMIN_PASSWORD = "admin_user_password"


@pytest.fixture(scope='module')
def app():
    os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
    app = create_app()

    # other setup can go here
    db.init_app(app)
    app.app_context().push()
    db.create_all()

    yield app

    # clean up / reset resources here
    db.session.remove()
    db.drop_all()


@pytest.fixture(scope='module')
def client(app):
    return app.test_client()


@pytest.fixture(scope='module')
def admin_user():
    user = UserModel(constants.TEST_AUTH_ADMIN_USERNAME, constants.TEST_AUTH_ADMIN_PASSWORD)
    user.save_to_db()
    return user


@pytest.fixture(scope='module')
def admin_user_tokens(admin_user):
    access_token = create_access_token(identity=admin_user.id, fresh=True)
    refresh_token = create_refresh_token(admin_user.id)
    return {
        'access_token': access_token,
        'refresh_token': refresh_token
    }


@pytest.fixture(scope='module')
def auth_user():
    user = UserModel(constants.TEST_AUTH_USER_USERNAME, constants.TEST_AUTH_USER_PASSWORD)
    user.save_to_db()
    return user


@pytest.fixture(scope='module')
def auth_user_tokens(auth_user):
    access_token = create_access_token(identity=auth_user.id, fresh=True)
    refresh_token = create_refresh_token(auth_user.id)
    return {
        'access_token': access_token,
        'refresh_token': refresh_token
    }


@pytest.fixture(scope='module')
def store(app):
    store = StoreModel(constants.TEST_STORE_NAME)
    store.save_to_db()
    return store


@pytest.fixture(scope='module')
def item(app):
    item = ItemModel(constants.TEST_ITEM_NAME, constants.TEST_ITEM_PRICE, constants.TEST_ITEM_STORE_ID)
    item.save_to_db()
    return item


@pytest.fixture(scope='module')
def user(app):
    user = UserModel(constants.TEST_USER_USERNAME, constants.TEST_USER_PASSWORD)
    user.save_to_db()
    return user
