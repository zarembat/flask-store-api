from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.item import ItemModel


class Item(Resource):
    # The parser will remove everything from the JSON payload which is not defined below
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Every item needs a store id."
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found.'}, 404

    @jwt_required()
    def post(self, name):
        # Check it the item with this name is not already in the database
        if ItemModel.find_by_name(name):
            return {'message': f'An item with the name "{name}" already exists.'}, 400
        
        data = Item.parser.parse_args()

        item = ItemModel(name, **data)
        
        try:
            item.save_to_db()
        except:
            return {"message": "An error occured when inserting the item."}, 500  # Internal Server Error

        return item.json(), 201  # 201 is for CREATED

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()  # instead of request.json or request.get_json()

        item = ItemModel.find_by_name(name)

        if not item:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
            item.store_id = data['store_id']

        item.save_to_db()
            
        return item.json()
        

class ItemList(Resource):
    def get(self):   
        return {'items': [item.json() for item in ItemModel.find_all]}
        # return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}  # same as above