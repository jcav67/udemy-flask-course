from flask import Flask
from flask_smorest import Api

from resources.item import item_bp as ItemBluePrint
from resources.store import blp as StoreBluePrint

app = Flask(__name__)

app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "Stores REST API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "1.0.0"
app.config["OPEN_URI_PREFIX"] = "/"
app.config["OPEN_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPEN_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

api = Api()
api.register_blueprint(ItemBluePrint)
api.register_blueprint(StoreBluePrint)
