import os
import json

from flask import Flask, request, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from logging.config import dictConfig

from db import db
from blocklist import BLOCKLIST
from models.user import UserModel

# SQLAlchemy creates tables based on those imports:
from resources.user import UserRegister, User, UserLogin, TokenRefresh, UserLogout
from resources.item import Item, ItemList
from resources.store import Store, StoreList


# Find the absolute file path to the top level project directory
basedir = os.path.abspath(os.path.dirname(__file__))


# Application factory
def create_app():
    app = Flask(__name__)

    # Configure Flask app
    CONFIG_TYPE = os.getenv('CONFIG_TYPE', default='config.DevelopmentConfig')
    app.config.from_object(CONFIG_TYPE)
    setup_claims(app)
    setup_endpoints(app)

    @app.before_first_request
    def create_tables():
        db.create_all()

    return app


def setup_endpoints(app):
    api = Api(app)

    api.add_resource(Store, '/store/<string:name>')
    api.add_resource(Item, '/item/<string:name>')
    api.add_resource(ItemList, '/items')
    api.add_resource(StoreList, '/stores')
    api.add_resource(UserRegister, '/register')
    api.add_resource(User, '/user/<int:user_id>')
    api.add_resource(UserLogin, '/auth')
    api.add_resource(UserLogout, '/logout')
    api.add_resource(TokenRefresh, '/refresh')


def setup_claims(app):

    jwt = JWTManager(app)

    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        user = UserModel.find_by_id(identity)
        if "admin" in user.username: # Just an example - instead of hard-coding, this should normally be read from some config
            return {'is_admin': True}
        return {'is_admin': False}

    @jwt.token_in_blocklist_loader
    def check_if_token_is_revoked(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        return jti in BLOCKLIST

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({
            'description': 'The token has expired.',
            'error': 'token_expired'
        }), 401


    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({
            'description': 'Signature verification failed.',
            'error': 'invalid_token'
        }), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({
            'description': 'Request does not contain an access token.',
            'error': 'authorization_required'
        }), 401

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return jsonify({
            'description': 'The token is not fresh.',
            'error': 'fresh_token_required'
        }), 401

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return jsonify({
            'description': 'The token has been revoked.',
            'error': 'token_revoked'
        }), 401


def configure_logging():
    # Read log config from file
    with open(os.path.join(basedir, 'config/log_config.json')) as log_file:
        config_dict = json.load(log_file)
        dictConfig(config_dict)


if __name__ == '__main__':
    app = create_app()
    configure_logging()
    db.init_app(app)
    app.logger.info("Starting application...")
    app.run()
    