import uuid

from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint,abort
from db import stores


blp = Blueprint("stores", __name__, description="Operations on stores")

@blp.route("/store/<string:store_id")
class Store(MethodView):

    def get(self,store_id):
        try:
            return stores[store_id]
        except KeyError:
            abort(404, message="Store not found")
    
    def delete(self,store_id):
        try:
            del stores[store_id]
            return {"message" :" store deleted"} 
        except KeyError:
            abort(404, message="Store not found")

@blp.route("/store")
class StoreList(MethodView):
    def get():
        return {"stores": list(stores.values())}
    
    def post():
        request_data = request.get_json()
        if not all(item in request_data for item in REQUEST_NEWSTORE_VALIDATION):
            abort(400, {"message":"Unvalid request body, please check information"})
        store_id = uuid.uuid4().hex

        new_store = {**request_data,"id":store_id}
        stores[store_id] = new_store
        return new_store,201
