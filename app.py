import os
from dotenv import load_dotenv

load_dotenv()  # must run before importing anything that reads env vars (services.s3)

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate

from db import db
from models import Supplier, Product, Listing  # noqa: F401 (imported so tables are registered)
from routes.products import products_bp
from routes.listings import listings_bp

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

# --- Database ---------------------------------------------------------------
# Production: DATABASE_URL must be set (Postgres). Local dev falls back to SQLite.
db_url = os.environ.get("DATABASE_URL")
if not db_url:
    if os.environ.get("APP_ENV") == "production":
        raise RuntimeError("DATABASE_URL is not set")
    db_url = "sqlite:///" + os.path.join(BASE_DIR, "trademach.db")

app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_pre_ping": True}

# Allow the Vue app to call this API
CORS(app, origins=os.environ.get("FRONTEND_ORIGIN", "http://localhost:5173").split(","))

db.init_app(app)
migrate = Migrate(app, db)  # enables `flask db init/migrate/upgrade`

app.register_blueprint(products_bp)
app.register_blueprint(listings_bp)

if __name__ == "__main__":
    app.run(debug=True, port=5000)