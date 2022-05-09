from models.item import ItemModel
from models.store import StoreModel
from models.user import UserModel


"""
GIVEN a Store model
WHEN a new Store is created
THEN check if the name is defined correctly
"""
def test_new_store(store: StoreModel):
    assert store.name == "Testing store"


"""
GIVEN an Item model
WHEN a new Item is created
THEN check if the name, price and store_id are defined correctly
"""
def test_new_item(item: ItemModel):
    assert item.name == "Item name"
    assert item.price == 99.99
    assert item.store_id == 1


"""
GIVEN a User model
WHEN a new User is created
THEN check if the username and password are defined correctly
"""
def test_new_user(user: UserModel):
    user = UserModel("Username", "Password")
    assert user.username == "Username"
    assert user.password == "Password"