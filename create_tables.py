from app import app
from db import db
from models import Supplier, Product, Listing  # noqa: F401

with app.app_context():
    db.create_all()  # creates only tables that don't exist yet
    print("Tables ready")