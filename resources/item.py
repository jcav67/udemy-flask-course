import uuid

from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint,abort
from db import items

item_bp = Blueprint("items", __name__, description = "Operations on items")

REQUEST_NEWITEM_VALIDATION= ("name", "price")

@item_bp.route("/items/<string:item_id>/")
class Items(MethodView):
    def get(self,item_id):

        try:
            return items[item_id],200
        except KeyError:
            return abort(404,{"message":"store not found"})  
        
    def delete(self,item_id):

        try:
            del items[item_id]
            return {"message":"item deleted"}
        except KeyError:
            return abort({"message":"store not found"})  


    def put(item_id):
        item_data = request.get_json()
        if not all(item in item_data for item in REQUEST_NEWITEM_VALIDATION):
            return abort(400,{"message":"Unvalid request body, please check information"})
        try:
            item = items[item_id]
            #dictionary item update
            item |= item_data
            return item
        except KeyError:
            return abort({"message":"item not found"})