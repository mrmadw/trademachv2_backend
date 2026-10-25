from db import db 
from datetime import datetime

class Listing(db.Model):
    __tablename__ = "listings"

    id = db.Column(db.Integer, primary_key=True)
    #product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    #product = db.relationship("Product", backref="listings")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    country = db.Column(db.String(100), nullable=False)
    province = db.Column(db.String(100))
    state = db.Column(db.String(100))
    city = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    po_box = db.Column(db.String(4), nullable=False)
    price = db.Column(db.Float, nullable=False)
    src_qty = db.Column(db.Integer)
    src_type = db.Column(db.String(10))
    pro_age = db.Column(db.Integer)

