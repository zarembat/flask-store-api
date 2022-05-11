from db import db

class StoreModel(db.Model):

    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel', lazy='dynamic')  # it tells SQLAlchemy that StoreModel has a relationship with ItemModel, additionally lazy initialization

    def __init__(self, name):
        self.name = name

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'items': [item.json() for item in self.items.all()]
            }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()  # will find a store by its name and return a StoreModel object

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):  # SQLAlchemy will upsert data
        db.session.add(self)  # we can add multiple objects to the session
        db.session.commit()  # and then commit in the end

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
