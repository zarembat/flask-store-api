import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username',
            type=str,
            required=True,
            help="Provide user name"
        )
        parser.add_argument('password',
            type=str,
            required=True,
            help="Provide user password"
        )

        data = parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "User already exists"}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created successfully."}
