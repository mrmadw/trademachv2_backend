from app import app
from models import Product

with app.app_context():
    print("DB:", app.config["SQLALCHEMY_DATABASE_URI"])
    print("Rows:", Product.query.count())