

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.secret_key = 'your_secret_key'
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(200))
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __str__(self):
        return self.name

@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/add_product', methods=['POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        quantity = int(request.form['quantity'])
        product = Product(name=name, description=description, price=price, quantity=quantity)
        db.session.add(product)
        db.session.commit()
        flash('Producto agregado con éxito.', 'success')
    return redirect(url_for('index'))

@app.route('/sell_product/<int:product_id>', methods=['POST'])
def sell_product(product_id):
    if request.method == 'POST':
        product = Product.query.get(product_id)
        quantity_sold = int(request.form['quantity_sold'])
        if quantity_sold <= product.quantity:
            product.quantity -= quantity_sold
            db.session.commit()
            flash('Venta realizada con éxito.', 'success')
        else:
            flash('No hay suficiente inventario disponible.', 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

