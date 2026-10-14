from flask import Blueprint, jsonify
from models import Listing
from services.s3 import image_url

listings_bp = Blueprint("listings", __name__)


@listings_bp.get("/api/listings")
def get_listings():
    listings = Listing.query.all()

    result = []

    for listing in listings:
        product = listing.product
        result.append({
            "id": listing.id,
            "product_id": listing.product_id,
            "product_name": product.name,
            "manufacturer": product.manufacturer,
            "model": product.model,
            "image_url": image_url(product.image_key),
            "country": listing.country,
            "province": listing.province,
            "state": listing.state,
            "city": listing.city,
            "address": listing.address,
            "po_box": listing.po_box,
            "price": listing.price,
            "src_qty": listing.src_qty,
            "src_type": listing.src_type,
            "pro_age": listing.pro_age,
            "created_at": listing.created_at.isoformat() if listing.created_at else None,
        })

    return jsonify(result)
