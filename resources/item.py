import uuid

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items
from schemas import ItemSchema, ItemUpdateSchema

item_bp = Blueprint("items", __name__, description="Operations on items")

REQUEST_NEWITEM_VALIDATION = ("name", "price")


@item_bp.route("/items/<string:item_id>/")
class Items(MethodView):
    @item_bp.response(200, ItemSchema)
    def get(self, item_id):
        try:
            return items[item_id], 200
        except KeyError:
            return abort(404, {"message": "store not found"})

    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": "item deleted"}
        except KeyError:
            return abort({"message": "store not found"})

    @item_bp.arguments(ItemUpdateSchema)
    @item_bp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        try:
            item = items[item_id]
            # dictionary item update
            item |= item_data
            return item
        except KeyError:
            return abort({"message": "item not found"})


@item_bp.route("/item")
class ItemList(MethodView):
    @item_bp.response(200, ItemSchema(many=True))
    def get(self):
        return items.values()

    # el segundo parametro es la data parseada por el schema
    @item_bp.arguments(ItemSchema)
    @item_bp.response(201, ItemSchema)
    def post(self, item_data):
        for item in items.values():
            if (
                item_data["name"] == item["and"]
                and item_data["store_id"] == item["store_id"]
            ):
                abort(400, message="item already exist.")

        item_id = uuid.uuid4().hex
        item = {**item_data, "id": item_id}
        items[item_id] = item

        return item
