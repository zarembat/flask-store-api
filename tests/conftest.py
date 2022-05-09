import pytest
import flask_testing

from flask import Flask
from db import db
from models.store import StoreModel
from models.item import ItemModel
from models.user import UserModel

@pytest.fixture()
def test_app():
    app = Flask(__name__)
    app.config.update({
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "TESTING": True
    })

    # other setup can go here
    db.init_app(app)
    with app.app_context():
        db.create_all()

    yield app

    # clean up / reset resources here
    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(test_app):
    return test_app.test_client()


@pytest.fixture()
def runner(test_app):
    return test_app.test_cli_runner()


@pytest.fixture(scope='module')
def store():
    store = StoreModel("Testing store")
    return store


@pytest.fixture(scope='module')
def item():
    item = ItemModel("Item name", 99.99, 1)
    return item


@pytest.fixture(scope='module')
def user():
    user = UserModel("Username", "Password")
    return user