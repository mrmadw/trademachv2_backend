from flask import Blueprint, jsonify
from models.product import Product
from services.s3 import image_url, s3, BUCKET
import uuid
from db import db

products_bp = Blueprint("products", __name__)


@products_bp.get("/api/products")
def get_products():
    products = Product.query.all()

    result = []

    for product in products:
        prices = [l.price for l in product.listings]
        result.append({
        "id": product.id,
        "name": product.name,
        "manufacturer": product.manufacturer,
        "model": product.model,
        "image_url": image_url(product.image_key),
        "price": min(prices) if prices else None,
        })

    return jsonify(result)


@products_bp.post("/api/products")
def create_product():
    name = request.form.get("name")
    supplier_id = request.form.get("supplier_id", type=int)
    if not name or not supplier_id:
        return jsonify(error="name and supplier_id are required"), 400

    image_key = None
    file = request.files.get("image")
    if file:
        ext = file.filename.rsplit(".", 1)[-1].lower()
        if ext not in {"jpg", "jpeg", "png", "webp"}:
            return jsonify(error="unsupported image type"), 400
        image_key = f"{uuid.uuid4().hex}.{ext}"
        s3.upload_fileobj(file, BUCKET, image_key,
                          ExtraArgs={"ContentType": file.mimetype})

    product = Product(
        name=name,
        manufacturer=request.form.get("manufacturer"),
        model=request.form.get("model"),
        image_key=image_key,
        supplier_id=supplier_id,
    )
    db.session.add(product)
    db.session.commit()
    return jsonify(id=product.id), 201

@products_bp.get("/api/products/<int:product_id>")
def get_product(product_id):
    product = db.get_or_404(Product, product_id)
    supplier = product.supplier

    return jsonify({
        "id": product.id,
        "name": product.name,
        "manufacturer": product.manufacturer,
        "model": product.model,
        "image_url": image_url(product.image_key),
        "supplier": {
            "name": supplier.name,
            "city": supplier.city,
            "country": supplier.country,
            "email": supplier.email,
            "contact_number": supplier.contact_number,
        },
        "listings": [
            {
                "id": l.id,
                "price": l.price,
                "city": l.city,
                "province": l.province,
                "country": l.country,
                "src_qty": l.src_qty,
                "src_type": l.src_type,
                "pro_age": l.pro_age,
            }
            for l in product.listings
        ],
    })