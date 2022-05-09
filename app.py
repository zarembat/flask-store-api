import os
import logging
import logging.config
import json

from flask import Flask, request, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from db import db
from configparser import ConfigParser

from blocklist import BLOCKLIST

# SQLAlchemy creates tables based on those imports:
from resources.user import UserRegister, User, UserLogin, TokenRefresh, UserLogout
from resources.item import Item, ItemList
from resources.store import Store, StoreList

# Read config from file
config = ConfigParser()
config.read('./config/app.ini')

# Read log config from file
with open(config['general']['log_config_file']) as log_file:
    config_dict = json.load(log_file)
    logging.config.dictConfig(config_dict)

logger = logging.getLogger(__name__)

app = Flask(__name__)

if os.environ.get('DATABASE_URL'):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace('postgres://', 'postgresql://') # workaround for Heroku's incorrect postgresql uri
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite://{config['sqlite']['data_file']}" # use SQLite as a default
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config['flask-sqlalchemy']['track_modifications']
app.config['PROPAGATE_EXCEPTIONS'] = config['flask']['propagate_exceptions']
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'tomek')

api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWTManager(app)

@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1: # Just an example - instead of hard-coding, this should normally be read from some config
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

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/auth')
api.add_resource(UserLogout, '/logout')
api.add_resource(TokenRefresh, '/refresh')

if __name__ == '__main__':
    db.init_app(app)
    logger.info("Starting application...")
    app.run(port=config['flask']['app_port'], debug=config['flask']['debug_enabled'])
    