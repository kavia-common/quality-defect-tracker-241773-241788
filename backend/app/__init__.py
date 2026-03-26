import os

from flask import Flask
from flask_cors import CORS
from flask_smorest import Api

from .routes.defects import blp as defects_blp
from .routes.health import blp as health_blp

app = Flask(__name__)
app.url_map.strict_slashes = False

# CORS configuration:
# The user request requires "Enable CORS for all origins" so the React frontend can
# reach the Flask backend in cloud/preview environments without origin mismatch.
#
# If you want to lock this down later, set CORS_ORIGINS to a comma-separated list
# of allowed origins (e.g. https://my-frontend.example.com).
cors_origins_env = os.environ.get("CORS_ORIGINS", "*").strip()
cors_origins = "*" if cors_origins_env == "*" else [o.strip() for o in cors_origins_env.split(",") if o.strip()]

CORS(
    app,
    resources={r"/*": {"origins": cors_origins}},
    supports_credentials=False,
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
    max_age=86400,
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
