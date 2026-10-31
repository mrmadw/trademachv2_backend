
import os
import uuid

import boto3
from botocore.config import Config
from botocore.exceptions import BotoCoreError, ClientError
from flask import Blueprint, jsonify, request

from auth_utils import admin_required
from db import db
from models.product import Product

uploads_bp = Blueprint("uploads", __name__)

# Extension comes from the validated content type, never from the user's filename.
ALLOWED_TYPES = {
    "image/jpeg": "jpg",
    "image/png": "png",
    "image/webp": "webp",
    "image/gif": "gif",
}


#endpoint
def _client(endpoint):
    return boto3.client(
        "s3",
        endpoint_url=endpoint,
        aws_access_key_id=os.environ["GARAGE_KEY_ID"],
        aws_secret_access_key=os.environ["GARAGE_SECRET_KEY"],
        region_name=os.environ.get("GARAGE_REGION", "garage"),
        config=Config(
            signature_version="s3v4",
            s3={"addressing_style": "path"},
            # Newer boto3 adds checksum headers by default; only send them when required.
            # (Needs botocore >= 1.36. If you get a TypeError here, upgrade boto3 or drop these two lines.)
            request_checksum_calculation="when_required",
            response_checksum_validation="when_required",
        ),
    )


def _internal():
    return _client(os.environ["GARAGE_ENDPOINT"])


def _public():
    # Presigned URLs embed the host in the signature, so sign with the address the browser will use.
    return _client(os.environ.get("GARAGE_PUBLIC_ENDPOINT") or os.environ["GARAGE_ENDPOINT"])


def bucket():
    return os.environ["GARAGE_BUCKET"]


def image_url(image_key, expires=3600):
    """Turn a stored image_key into a temporary URL. Use this in GET /api/products."""
    if not image_key:
        return None
    return _public().generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket(), "Key": image_key},
        ExpiresIn=expires,
    )


def _delete_object(key):
    try:
        _internal().delete_object(Bucket=bucket(), Key=key)
    except (BotoCoreError, ClientError):
        pass  # best effort; an orphaned object is better than a failed request


@uploads_bp.post("/products/<int:product_id>/image")
@admin_required
def upload_product_image(product_id):
    product = db.session.get(Product, product_id)
    if product is None:
        return jsonify(error="Product not found"), 404

    file = request.files.get("image")
    if file is None or file.filename == "":
        return jsonify(error="No file sent. Use multipart form field 'image'."), 400

    ext = ALLOWED_TYPES.get(file.mimetype)
    if ext is None:
        return jsonify(error=f"Unsupported type. Allowed: {', '.join(ALLOWED_TYPES)}"), 415

    new_key = f"products/{product_id}/{uuid.uuid4().hex}.{ext}"
    old_key = product.image_key

    try:
        _internal().upload_fileobj(
            file.stream,
            bucket(),
            new_key,
            ExtraArgs={"ContentType": file.mimetype},
        )
    except (BotoCoreError, ClientError) as exc:
        return jsonify(error="Storage upload failed", detail=str(exc)), 502

    product.image_key = new_key
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        _delete_object(new_key)  # don't leave an object nothing points at
        raise

    if old_key:
        _delete_object(old_key)

    return jsonify(image_key=new_key, image_url=image_url(new_key)), 201


@uploads_bp.delete("/products/<int:product_id>/image")
@admin_required
def delete_product_image(product_id):
    product = db.session.get(Product, product_id)
    if product is None:
        return jsonify(error="Product not found"), 404
    if not product.image_key:
        return "", 204

    old_key = product.image_key
    product.image_key = None
    db.session.commit()
    _delete_object(old_key)
    return "", 204