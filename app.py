import os

from flask import Flask, request, jsonify
from flask_restful import Api
from flask_jwt_extended import create_access_token, JWTManager
from db import db

from security import authenticate
# SQLAlchemy creates tables based on those imports:
from resources.user import UserRegister, User
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db').replace('postgres://', 'postgresql://')  # workaround for Heroku's incorrect postgresql uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_SECRET_KEY'] = 'tomek'  # this is secret!

api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWTManager(app)

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')

@app.route('/auth', methods=['POST'])
def auth():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if authenticate(username, password):
        return jsonify(access_token=create_access_token(identity=username))
    else:
        return {"message": "Invalid credentials"}, 401

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
    