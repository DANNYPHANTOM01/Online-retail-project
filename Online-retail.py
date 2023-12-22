from flask import Flask, render_template, request, redirect, url_for, session
import json
import hashlib

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secret key for session security

class OnlineRetailSystem:
    def __init__(self):
        self.users = {}
        self.products = {'1001': {'name': 'Product 1', 'price': 20},
                         '1002': {'name': 'Product 2', 'price': 30},
                         '1003': {'name': 'Product 3', 'price': 25}}

    def register_user(self, username, password):
        # Simulate user registration
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        self.users[username] = {'password': hashed_password, 'cart': {}}

    def login_user(self, username, password):
        # Simulate user login
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if username in self.users and self.users[username]['password'] == hashed_password:
            session['username'] = username
            return True
        else:
            return False

    def logout_user(self):
        # Simulate user logout
        session.pop('username', None)

    def display_catalog(self):
        # Display product catalog
        return [(product_id, product_info['name'], product_info['price']) for product_id, product_info in self.products.items()]

    def add_to_cart(self, product_id, quantity):
        # Simulate adding products to the user's cart
        username = session.get('username')
        if product_id in self.products and username in self.users:
            if product_id in self.users[username]['cart']:
                self.users[username]['cart'][product_id] += quantity
            else:
                self.users[username]['cart'][product_id] = quantity

    def get_cart(self):
        # Get the user's cart
        username = session.get('username')
        if username in self.users:
            return self.users[username]['cart']
        return {}

    def checkout(self):
        # Simulate a secure transaction and checkout process
        username = session.get('username')
        if username in self.users:
            total_price = sum(self.products[product_id]['price'] * quantity for product_id, quantity in self.users[username]['cart'].items())
            return total_price
        return 0

online_retail_system = OnlineRetailSystem()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if online_retail_system.login_user(username, password):
            return redirect(url_for('catalog'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    online_retail_system.logout_user()
    return redirect(url_for('home'))

@app.route('/catalog')
def catalog():
    products = online_retail_system.display_catalog()
    return render_template('catalog.html', products=products)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = request.form['product_id']
    quantity = int(request.form['quantity'])
    online_retail_system.add_to_cart(product_id, quantity)
    return redirect(url_for('catalog'))

@app.route('/cart')
def cart():
    cart = online_retail_system.get_cart()
    return render_template('cart.html', cart=cart, products=online_retail_system.products)

@app.route('/checkout')
def checkout():
    total_price = online_retail_system.checkout()
    return render_template('checkout.html', total_price=total_price)

if __name__ == '__main__':
    app.run(debug=True)