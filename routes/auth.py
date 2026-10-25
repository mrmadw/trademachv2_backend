


from db import db
from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token, get_jwt, get_jwt_identity, jwt_required,
    set_access_cookies, unset_jwt_cookies,
)
from werkzeug.security import check_password_hash

from models.user import Admin 

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/api/auth/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    admin = db.session.execute(
        db.select(Admin).filter_by(email=email)
    ).scalar_one_or_none()

    # same message for unknown email and wrong password
    if admin is None or not check_password_hash(admin.password_hash, password):
        return jsonify({"error": "Invalid email or password"}), 401

    token = create_access_token(identity=str(admin.id))
    resp = jsonify({"id": admin.id, "email": admin.email})
    set_access_cookies(resp, token)
    return resp, 200


@auth_bp.route("/api/auth/logout", methods=["POST"])
def logout():
    resp = jsonify({"message": "Logged out"})
    unset_jwt_cookies(resp)
    return resp, 200


@auth_bp.route("/api/auth/me", methods=["GET"])
@jwt_required()
def me():
    admin = db.session.get(Admin, int(get_jwt_identity()))
    if admin is None:
        return jsonify({"error": "Account no longer exists"}), 401
    return jsonify({"id": admin.id, "email": admin.email, "csrf": get_jwt()["csrf"]}), 200