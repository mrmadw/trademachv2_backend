from flask import Blueprint, jsonify, request
from db import db
from models.product import Product
from auth_utils import admin_required

products_bp = Blueprint("products", __name__)


@products_bp.route("/products", methods=["GET"])
@admin_required
def get_products():
    products = db.session.execute(
        db.select(Product)
    ).scalars().all()

    return jsonify([
        {
            "id": p.id,
            "name": p.name,
            "manufacturer": p.manufacturer,
            "model": p.model,
            "supplier_id": p.supplier_id,
        }
        for p in products
    ])


@products_bp.route("/products", methods=["POST"])
@admin_required
def create_product():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "A JSON object is required"}), 400

    name = data.get("name")

    if not isinstance(name, str) or not name.strip():
        return jsonify({"error": "Product name is required"}), 400

    product = Product(
        name=name.strip(),
        manufacturer=data.get("manufacturer"),
        model=data.get("model"),
        supplier_id=data.get("supplier_id"),
    )

    db.session.add(product)
    db.session.commit()

    return jsonify({
        "id": product.id,
        "name": product.name,
        "manufacturer": product.manufacturer,
        "model": product.model,
        "supplier_id":product.supplier_id,
    }), 201



@products_bp.route('/products/<int:product_id>', methods=['DELETE'])
@admin_required
def delete_product(product_id):
    product = db.session.get(Product, product_id)
    if product is None:
        return jsonify({"error": "Product not found"}), 404

    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted"}), 200