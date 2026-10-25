from db import db 
from werkzeug.security import generate_password_hash, check_password_hash

class Admin(db.Model):
	__tablename__ = "admin_users"

	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(120), unique=True, nullable=False)
	password_hash = db.Column(db.String(255), nullable=False)
	is_active = db.Column(db.Boolean, nullable=False, default=True)

	def set_password(self, pw):
		self.password_hash = generate_password_hash(pw)

	def check_password_hash(self, pw):
		return check_password_hash(self.password_hash, pw)