from flask import Blueprint, jsonify, request
from db import db
from models.listing import Listing
from auth_utils import admin_required

listings_bp = Blueprint("listings", __name__)


@listings_bp.route("/listings", methods=["GET"])
def get_listings():
    listings = db.session.execute(
        db.select(Listing)
    ).scalars().all()

    return jsonify([
        {
            "id": l.id,
            "city": l.city,
            "province": l.province,
            "address": l.address
        }
        for l in listings
    ])


@listings_bp.route("/listings", methods=["POST"])
@admin_required
def create_listing():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "A JSON object is required"}), 400

    name = data.get("name")

    if not isinstance(address, str) or not address.strip():
        return jsonify({"error": "listing address is required"}), 400

    listing = Listing(
        name=name.strip(),
        manufacturer=data.get("manufacturer"),
        model=data.get("model")
    )

    db.session.add(product)
    db.session.commit()

    return jsonify({
        "id": listing.id,
        "city": listing.city,
        "province": listing.province,
        "address": listing.address
    }), 201


@listings_bp.route('/listings/<int:listing_id>', methods=['DELETE'])
@admin_required
def delete_listing(listing_id):
    listing = db.session.get(Listing, listing_id)
    if listing is None:
        return jsonify({"error": "Listing not found"}), 404

    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Listing deleted"}), 200