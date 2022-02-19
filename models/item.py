from db import db

class ItemModel(db.Model):

    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))  # this tells SQLAlchemy that items are assigned to stores and this is the foreign key
    store = db.relationship('StoreModel')  # we define a relationship

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()  # will find an item by its name and return an ItemModel object

    def save_to_db(self):  # SQLAlchemy will upsert data
        db.session.add(self)  # we can add multiple objects to the session
        db.session.commit()  # and then commit in the end

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
