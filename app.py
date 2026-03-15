from flask import Flask, render_template, request, redirect, url_for
from models import db, Product, Bill, BillItem

app = Flask(__name__)

# ----------------------------
# DATABASE CONFIG
# ----------------------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# ----------------------------
# DASHBOARD (HOME PAGE)
# ----------------------------
@app.route('/')
def dashboard():
    products = Product.query.all()

    total_products = len(products)
    total_units_sold = sum(p.units_sold for p in products)
    total_revenue = sum(p.total_revenue for p in products)

    top_product = None
    if products:
        top_product = max(products, key=lambda p: p.units_sold)

    chart_labels = [p.name for p in products]
    chart_data = [p.units_sold for p in products]

    return render_template(
        'dashboard.html',
        total_products=total_products,
        total_units_sold=total_units_sold,
        total_revenue=total_revenue,
        top_product=top_product,
        chart_labels=chart_labels,
        chart_data=chart_data
    )

# ----------------------------
# PRODUCTS PAGE
# ----------------------------
@app.route('/products')
def products():
    all_products = Product.query.all()
    return render_template('products.html', products=all_products)

# ----------------------------
# ADD PRODUCT
# ----------------------------
@app.route('/add_product', methods=['POST'])
def add_product():
    try:
        name = request.form.get('name')
        category = request.form.get('category') or "General"

        price = float(request.form.get('price') or 0)
        quantity = int(request.form.get('quantity') or 0)
        low_stock_limit = int(request.form.get('low_stock_limit') or 0)

        new_product = Product(
            name=name,
            category=category,
            price=price,
            quantity=quantity,
            low_stock_limit=low_stock_limit
        )

        db.session.add(new_product)
        db.session.commit()

        return redirect(url_for('products'))

    except Exception as e:
        return f"Error adding product: {str(e)}"

# ----------------------------
# DELETE PRODUCT
# ----------------------------
@app.route('/delete_product/<int:id>')
def delete_product(id):
    product = Product.query.get_or_404(id)

    if product.bill_items:
        return "Cannot delete product with sales history"

    db.session.delete(product)
    db.session.commit()

    return redirect(url_for('products'))

# ----------------------------
# CREATE BILL
# ----------------------------
@app.route('/create_bill', methods=['GET', 'POST'])
def create_bill():
    products = Product.query.all()

    if request.method == 'POST':
        total_amount = 0
        bill = Bill(total_amount=0)
        db.session.add(bill)
        db.session.flush()

        for product in products:
            qty = request.form.get(f'quantity_{product.id}')

            if qty and int(qty) > 0:
                qty = int(qty)

                if qty <= product.quantity:
                    product.quantity -= qty
                    product.units_sold += qty
                    product.total_revenue += qty * product.price

                    bill_item = BillItem(
                        bill_id=bill.id,
                        product_id=product.id,
                        quantity=qty,
                        price_at_sale=product.price
                    )

                    db.session.add(bill_item)
                    total_amount += qty * product.price

        bill.total_amount = total_amount
        db.session.commit()

        return redirect(url_for('sales'))

    return render_template('create_bill.html', products=products)

# ----------------------------
# SALES HISTORY
# ----------------------------
@app.route('/sales')
def sales():
    bills = Bill.query.order_by(Bill.created_at.desc()).all()
    return render_template('sales.html', bills=bills)

# ----------------------------
# BILL DETAILS
# ----------------------------
@app.route('/bill/<int:bill_id>')
def bill_detail(bill_id):
    bill = Bill.query.get_or_404(bill_id)
    return render_template('bill_detail.html', bill=bill)

# ----------------------------
# RUN APP
# ----------------------------
if __name__ == '__main__':
    app.run(debug=True)