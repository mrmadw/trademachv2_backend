import os

from flask import Flask
from flask_cors import CORS

from db import db
import models
from models.product import Product
from routes.products import products_bp
from routes.listings import listings_bp
from routes.suppliers import suppliers_bp
from routes.auth import auth_bp
from routes.admin_users import adminusers_bp
from flask_migrate import Migrate
from dotenv import load_dotenv
from datetime import datetime, timedelta
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)


app.config["JWT_SECRET_KEY"] = os.environ["JWT_SECRET_KEY"] 
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_SECURE"] = os.environ.get("APP_ENV") == "production"
app.config["JWT_COOKIE_SAMESITE"] = "Lax"
app.config["JWT_COOKIE_CSRF_PROTECT"] = True
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=8)

JWTManager(app)
app.register_blueprint(auth_bp)

# --- Database ---------------------------------------------------------------
# Production: DATABASE_URL must be set (Postgres). Local dev falls back to SQLite.
db_url = os.environ.get("DATABASE_URL")
if not db_url:
    if os.environ.get("APP_ENV") == "production":
        raise RuntimeError("DATABASE_URL is not set")
    db_url = "sqlite:///" + os.path.join(BASE_DIR, "trademachv2.db")

app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_pre_ping": True}

# Allow the Vue app to call this API
CORS(app, origins=os.environ.get("FRONTEND_ORIGIN", "http://localhost:5173").split(","))

db.init_app(app)
migrate = Migrate(app, db)  # enables `flask db init/migrate/upgrade`

app.register_blueprint(products_bp)
app.register_blueprint(listings_bp)
app.register_blueprint(adminusers_bp)
app.register_blueprint(suppliers_bp)

if __name__ == "__main__":
    app.run(debug=True, port=5000)