
from db import db

class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    manufacturer = db.Column(db.String(100))
    model = db.Column(db.String(100))

    image_key = db.Column(db.String(500), nullable=True)

    #supplier_id = db.Column(db.Integer, db.ForeignKey("suppliers.id"), nullable=False)
    #supplier = db.relationship("Supplier", backref="products")


    