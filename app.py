from flask import Flask, request
from db import items, stores
import uuid

app = Flask(__name__)


@app.get("/store")
def get_stores():
    return {"stores": list(stores.values())}

@app.get("/item")
def get_all_items():
    return {"items": list(items.values())}

@app.post('/store')
def create_stores():
    store_data = request.get_json()
    store_id = uuid.uuid4().hex
    new_store = {**store_data, "id": store_id}
    stores[store_id] = new_store
    return new_store, 201


@app.post('/item')
def create_item(name):
    item_data = request.get_json()
    if item_data["store_id"] not in stores:
        return {"message": "Store not found"}, 404
    
    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    items[item_id] = item

    return item, 201


@app.get("/store/<string:name>")
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        return {"message": "Store not found"}, 404


@app.get("/item/<string:item_id>")
def get_item(name):
    try:
        return items[item_id]
    except KeyError:
        return {"message": "Store not found"}, 404