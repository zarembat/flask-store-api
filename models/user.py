import sqlite3
from db import db

class UserModel(db.Model):

    __tablename__ = 'users'  # this is how we tell SQLAlchemy what table this object should be mapped to

    # Column configuration for SQLAlchemy, their names match exactly object attributes (self.id etc.)
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()  # will find an item by its name and return a UserModel object

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()  # will find an item by its ID and return a UserModel object