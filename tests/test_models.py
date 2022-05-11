from flask import Flask


from tests import test_defaults
from models.item import ItemModel
from models.store import StoreModel
from models.user import UserModel


"""
GIVEN a Store model
WHEN a new store is created
THEN check if the name is defined correctly
"""
def test_new_store(store: StoreModel):
    assert store.name == test_defaults.TEST_STORE_NAME


"""
GIVEN an Item model
WHEN a new item is created
THEN check if the name, price and store_id are defined correctly
"""
def test_new_item(item: ItemModel):
    assert item.name == test_defaults.TEST_ITEM_NAME
    assert item.price == test_defaults.TEST_ITEM_PRICE
    assert item.store_id == test_defaults.TEST_ITEM_STORE_ID


"""
GIVEN an Item model
WHEN a new item is created
THEN check if it is assigned to the right store
"""
def test_get_store_for_item(item: ItemModel):
    assert item.store.name == test_defaults.TEST_STORE_NAME


"""
GIVEN an Item model
WHEN a new item is created
THEN check if it is assigned the right ID
"""
def test_item_id(item: ItemModel):
    assert item.id == 1


"""
GIVEN a Store model
WHEN a new store is created
THEN check if it is assigned the right ID
"""
def test_store_id(store: StoreModel):
    assert store.id == 1


"""
GIVEN a User model
WHEN a new user is created
THEN check if the username and password are defined correctly
"""
def test_new_user(user: UserModel):
    assert user.username == test_defaults.TEST_USER_USERNAME
    assert user.password == test_defaults.TEST_USER_PASSWORD


"""
GIVEN a User model
WHEN a new user is created
THEN check if it is assigned the right ID
"""
def test_user_id(user: UserModel):
    assert user.id == 1


"""
GIVEN a User model
WHEN a user ID is given
THEN check if a user can be found by ID
"""
def test_find_user_by_id():
    user = UserModel.find_by_id(1)
    test_new_user(user)


"""
GIVEN a User model
WHEN a username is given
THEN check if a user can be found by username
"""
def test_find_user_by_username():
    user = UserModel.find_by_username(test_defaults.TEST_USER_USERNAME)
    test_new_user(user)


"""
GIVEN a Store model
WHEN a store name is given
THEN check if a store can be found by name
"""
def test_find_store_by_name():
    store = StoreModel.find_by_name(test_defaults.TEST_STORE_NAME)
    test_new_store(store)


"""
GIVEN an Item model
WHEN an item name is given
THEN check if an item can be found by name
"""
def test_find_item_by_name():
    item = ItemModel.find_by_name(test_defaults.TEST_ITEM_NAME)
    test_new_item(item)


"""
GIVEN a Store model
THEN check if all stores can be retrieved
"""
def test_find_all_stores():
    assert len(StoreModel.find_all()) == 1


"""
GIVEN an Item model
THEN check if all items can be retrieved
"""
def test_find_all_items():
    assert len(ItemModel.find_all()) == 1