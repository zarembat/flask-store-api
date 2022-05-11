import pytest


from flask import Flask

from tests import test_defaults
from db import db
from models.store import StoreModel
from models.item import ItemModel
from models.user import UserModel


@pytest.fixture(scope="package")
def test_app():
    app = Flask(__name__)
    app.config.update({
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": True,
        "TESTING": True
    })

    # other setup can go here
    db.init_app(app)
    app.app_context().push()
    db.create_all()

    yield app

    # clean up / reset resources here
    db.session.remove()
    db.drop_all()


@pytest.fixture(scope="package")
def client(test_app):
    return test_app.test_client()


@pytest.fixture(scope="package")
def runner(test_app):
    return test_app.test_cli_runner()


@pytest.fixture(scope="package")
def store(test_app):
    store = StoreModel(test_defaults.TEST_STORE_NAME)
    store.save_to_db()
    return store


@pytest.fixture(scope="package")
def item(test_app):
    item = ItemModel(test_defaults.TEST_ITEM_NAME, test_defaults.TEST_ITEM_PRICE, test_defaults.TEST_ITEM_STORE_ID)
    item.save_to_db()
    return item


@pytest.fixture(scope="package")
def user(test_app):
    user = UserModel(test_defaults.TEST_USER_USERNAME, test_defaults.TEST_USER_PASSWORD)
    user.save_to_db()
    return user