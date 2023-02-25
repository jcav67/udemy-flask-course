from flask import Flask, jsonify,request
from db import stores,items
import uuid

app = Flask(__name__)

REQUEST_NEWSTORE_VALIDATION= ("name", "items")
REQUEST_NEWITEM_VALIDATION= ("name", "price")



@app.get("/store")
def get_stores():
    return {"stores": list(stores.values())}

@app.post("/store")
def create_store():
    request_data = request.get_json()
    if not all(item in request_data for item in REQUEST_NEWSTORE_VALIDATION):
        return jsonify({"message":"Unvalid request body, please check information"}),400
    store_id = uuid.uuid4().hex

    new_store = {**request_data,"id":store_id}
    stores[store_id] = new_store
    return new_store,201

@app.post("/item")
def create_item():
    request_data = request.get_json()

    if not all(item in request_data for item in REQUEST_NEWITEM_VALIDATION):
        return jsonify({"message":"Unvalid request body, please check information"}),400

    item_id = uuid.uuid4().hex
    new_item={**request_data,"id":item_id}
    items[item_id]=new_item
    return new_item,201

@app.get("/items")
def get_all_items():
    return {"items": list(items.values())}

@app.get("/store/<string:store_id>/store-by-name")
def get_store_by_name(store_id):
    try:
        return stores[store_id],201
    except:
        return jsonify({"message":"store not found"}),404

@app.get("/items/<string:item_id>/")
def get_items(item_id):

    try:
        return items[item_id],200
    except KeyError:
        return jsonify({"message":"store not found"}),404   
    

@app.delete("/items/<string:item_id>/")
def delete_items(item_id):

    try:
        del items[item_id]
        return {"message":"item deleted"}
    except KeyError:
        return jsonify({"message":"store not found"}),404  

    
@app.put("/items/<string:item_id>/")
def update_items(item_id):
    item_data = request.get_json()
    if not all(item in item_data for item in REQUEST_NEWITEM_VALIDATION):
        return jsonify({"message":"Unvalid request body, please check information"}),400
    try:
        item = items[item_id]
        item |= item_data
        return item
    except KeyError:
        return jsonify({"message":"item not found"}),404