import uuid

from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores

from schemas import StoreSchema


blp = Blueprint("stores", __name__, description="Operations on stores")

REQUEST_NEWSTORE_VALIDATION = ["name", "items"]


@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            abort(404, message="Store not found")

    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"message": " store deleted"}
        except KeyError:
            abort(404, message="Store not found")


@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(
        self,
    ):
        return {"stores": list(stores.values())}

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        for store in stores.values():
            if store_data["name"] == store["name"]:
                abort(400, message="Store already exist.")
        store_id = uuid.uuid4().hex

        new_store = {**store_data, "id": store_id}
        stores[store_id] = new_store
        return new_store, 201
