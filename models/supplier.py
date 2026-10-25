
from db import db
from datetime import datetime

class Supplier(db.Model):
    __tablename__ = "suppliers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    province = db.Column(db.String(100))
    state = db.Column(db.String(100))
    city = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    po_box = db.Column(db.String(4), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    contact_number = db.Column(db.String(10), nullable=False)
    contract_status = db.Column(db.String(20), nullable=False, default="active")
    rating = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)