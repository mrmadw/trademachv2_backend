from app import app
from db import db
from models import Supplier, Product, Listing

with app.app_context():
    if Product.query.count() > 0:
        print("Products already exist, nothing seeded.")
    else:
        supplier = Supplier.query.first()
        if not supplier:
            supplier = Supplier(
                name="TradeMach",
                country="Papua New Guinea",
                city="Port Moresby",
                address="Test Street",
                po_box="0001",
                email="supplier@example.com",
                contact_number="0000000000",
            )
            db.session.add(supplier)
            db.session.commit()

        p1 = Product(name="PC300", manufacturer="Komatsu", model="PC300",
                     image_key="00001-pc300-pom.jpeg", supplier_id=supplier.id)
        p2 = Product(name="PC210", manufacturer="Komatsu", model="PC210",
                     image_key="00002-pc210-lae.jpeg", supplier_id=supplier.id)
        db.session.add_all([p1, p2])
        db.session.commit()

        db.session.add_all([
            Listing(product_id=p1.id, country="Papua New Guinea", city="Port Moresby",
                    address="Test Street", po_box="0001", price=250000.0),
            Listing(product_id=p2.id, country="Papua New Guinea", city="Lae",
                    address="Test Street", po_box="0002", price=180000.0),
        ])
        db.session.commit()
        print("Seeded:", Product.query.count(), "products")