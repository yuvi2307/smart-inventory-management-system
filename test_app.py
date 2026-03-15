from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/test_inventory'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

class Bill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_amount = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    items = db.relationship('BillItem', backref='bill')

class BillItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bill_id = db.Column(db.Integer, db.ForeignKey('bill.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer)
    price_at_sale = db.Column(db.Float)

    product = db.relationship('Product')

with app.app_context():
    try:
        db.drop_all()
        db.create_all()

        p = Product(name="Test Product")
        db.session.add(p)
        db.session.commit()

        b = Bill(total_amount=100)
        db.session.add(b)
        db.session.commit()

        item = BillItem(bill_id=b.id, product_id=p.id, quantity=2, price_at_sale=50)
        db.session.add(item)
        db.session.commit()

        bill = Bill.query.first()
        print("Quantity:", bill.items[0].quantity)
        print("Product:", bill.items[0].product.name)

    except Exception as e:
        print("ERROR:", e)