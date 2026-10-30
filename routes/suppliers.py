from flask import Blueprint, jsonify, request
from db import db
from models.supplier import Supplier
from auth_utils import admin_required

suppliers_bp = Blueprint("suppliers", __name__)

@suppliers_bp.route("/api/suppliers", methods=["GET"])
@admin_required
def get_suppliers():
	suppliers = db.session.execute(
	db.select(Supplier)
	).scalars().all()

	return jsonify([
	{
	"id": s.id,
	"name": s.name,
	"country": s.country,
	"province": s.province,
	"state": s.state,
	"city": s.city,
	"address": s.address,
	"po_box": s.po_box,
	"email": s.email,
	"contact_number": s.contact_number,
	"rating": s.rating,
	"contract_status": s.contract_status,
	"created_at": s.created_at
	}
	for s in suppliers
	])

@suppliers_bp.route("/api/suppliers", methods=["POST"])
@admin_required
def create_product():
	data = request.get_json(silent=True)

	if not isinstance(data, dict):
		return jsonify({"error": "A JSON object is required"}), 400

	name = data.get("name")

	if not isinstance(name, str) or not name.strip():
		return jsonify({"error": "Supplier name is required"}), 400


	supplier = Supplier(
		name = name.strip(),
		email = data.get("email"),
		city = data.get("city")
		)

	db.session.add(supplier)
	db.session.commit()

	return jsonify({
	"id": supplier.id,
	"name": supplier.name,
	"email": supplier.email,
	"city": supplier.city
	}), 201

@suppliers_bp.route('/api/route/suppliers<int:supplier_id>', methods = ['DELETE'])
@admin_required
def delete_supplier(supplier_id):
	supplier = db.session.get(Supplier, supplier_id)
	if supplier is None:
		return jsonify({"error": "Supplier not found"}), 404

	db.session.delete(supplier)
	db.session.commit()
	return jsonify({"message": "Supplier deleted"}), 200