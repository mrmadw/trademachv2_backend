from db import db
from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash

from auth_utils import admin_required
from models.user import Admin

adminusers_bp = Blueprint("admins", __name__)

def serialize(admin):
    return {"id": admin.id, "email": admin.email}


def email_taken(email, exclude_id=None):
    query = db.select(Admin).filter_by(email=email)
    found = db.session.execute(query).scalar_one_or_none()
    return found is not None and found.id != exclude_id


@adminusers_bp.route("/api/admin_users", methods=["GET"])
@admin_required
def get_admins():
    admins = db.session.execute(db.select(Admin)).scalars().all()
    return jsonify([serialize(a) for a in admins])



@adminusers_bp.route("/api/admin_users", methods=["POST"])
@admin_required
def create_admin():
    
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify({"error": "email and password are required"}), 400
    if len(password) < 8:
        return jsonify({"error": "password must be at least 8 characters"}), 400
    if email_taken(email):
        return jsonify({"error": "email already in use"}), 409

    admin = Admin(email=email, password_hash=generate_password_hash(password))
    db.session.add(admin)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "email already in use"}), 409
    return jsonify(serialize(admin)), 201


@adminusers_bp.route("/api/admin_users/<int:adminuser_id>", methods=["PUT"])
@admin_required
def put_admin(adminuser_id):
    admin = db.session.get(Admin, adminuser_id)
    if admin is None:
        return jsonify({"error": "Admin not found"}), 404

    data = request.get_json(silent=True) or {}

    if "email" in data:
        email = (data["email"] or "").strip().lower()
        if not email:
            return jsonify({"error": "email cannot be empty"}), 400
        if email_taken(email, exclude_id=admin.id):
            return jsonify({"error": "email already in use"}), 409
        admin.email = email

    if data.get("password"):
        if len(data["password"]) < 8:
            return jsonify({"error": "password must be at least 8 characters"}), 400
        admin.password_hash = generate_password_hash(data["password"])

    db.session.commit()
    return jsonify(serialize(admin)), 200


@adminusers_bp.route("/api/admin_users/<int:adminuser_id>", methods=["DELETE"])
@admin_required
def delete_admin(adminuser_id):
    admin = db.session.get(Admin, adminuser_id)
    if admin is None:
        return jsonify({"error": "Admin not found"}), 404

    total = db.session.scalar(db.select(db.func.count()).select_from(Admin))
    if total <= 1:
        return jsonify({"error": "cannot delete the last admin"}), 400

    db.session.delete(admin)
    db.session.commit()
    return jsonify({"message": "Admin deleted"}), 200