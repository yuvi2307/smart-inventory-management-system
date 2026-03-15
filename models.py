from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# ---------------------------
# PRODUCT MODEL
# ---------------------------
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    category = db.Column(db.String(100))
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    low_stock_limit = db.Column(db.Integer)

    units_sold = db.Column(db.Integer, default=0)
    total_revenue = db.Column(db.Float, default=0)

    bill_items = db.relationship('BillItem', backref='product', lazy=True)

    # relationship to BillItem
    bill_items = db.relationship('BillItem', backref='product', lazy=True)

# ---------------------------
# BILL MODEL
# ---------------------------
class Bill(db.Model):
    __tablename__ = 'bill'

    id = db.Column(db.Integer, primary_key=True)
    total_amount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # relationship to BillItem
    items = db.relationship('BillItem', backref='bill', lazy=True)

# ---------------------------
# BILL ITEM MODEL
# ---------------------------
class BillItem(db.Model):
    __tablename__ = 'bill_item'

    id = db.Column(db.Integer, primary_key=True)
    bill_id = db.Column(db.Integer, db.ForeignKey('bill.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price_at_sale = db.Column(db.Float, nullable=False)