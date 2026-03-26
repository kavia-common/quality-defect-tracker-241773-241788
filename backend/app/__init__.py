import os

from flask import Flask
from flask_cors import CORS
from flask_smorest import Api

from .routes.defects import blp as defects_blp
from .routes.health import blp as health_blp

app = Flask(__name__)
app.url_map.strict_slashes = False

# CORS configuration (demo-safe):
# - Default allow React dev server at http://localhost:3000
# - Allow override via FRONTEND_URL env var (or REACT_APP_FRONTEND_URL if used)
frontend_url = os.environ.get("FRONTEND_URL") or os.environ.get("REACT_APP_FRONTEND_URL") or "http://localhost:3000"
CORS(
    app,
    resources={r"/*": {"origins": [frontend_url]}},
    supports_credentials=False,
)

app.config["API_TITLE"] = "My Flask API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/docs"
app.config["OPENAPI_SWAGGER_UI_PATH"] = ""
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

api = Api(app)
api.register_blueprint(health_blp)
api.register_blueprint(defects_blp)
