from database import db
from products import Product
from carts import Cart
import secrets
from flask import Flask, jsonify, request, session, redirect, url_for, flash, render_template
from flask_bcrypt import Bcrypt
import re
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)

secret_key = secrets.token_hex(16)
app.secret_key = secret_key

bcrypt = Bcrypt(app)

# Email validation function
def is_valid_email(email):
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(regex, email)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup', methods=['POST'])
def signup():
    email = request.json.get('email')
    password = request.json.get('password')

    if not is_valid_email(email):
        return jsonify({'message': 'Invalid email format. Please enter a valid email address.'}), 400

    cur = db.cursor()
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    existing_user = cur.fetchone()

    if existing_user:
        return jsonify({'message': 'Email already exists. Please choose a different email.'}), 400
    else:
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        cur.execute("INSERT INTO users (email, password_hash) VALUES (%s, %s)", (email, password_hash))
        db.commit()
        cur.close()
        return redirect(url_for('home'))

@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    if not is_valid_email(email):
        return jsonify({'message': 'Invalid email format. Please enter a valid email address.'}), 400

    cur = db.cursor()
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cur.fetchone()
    cur.close()

    if user and bcrypt.check_password_hash(user[2], password):
        session['user_id'] = user[0]
        session['email'] = user[1]
        return jsonify({'message': 'Login successful', 'user_id': user[0], 'email': user[1]})
    else:
        return jsonify({'message': 'Login unsuccessful. Please check email and password.'}), 401

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'You have been logged out.'}), 200

@app.route('/session_data', methods=['GET'])
def session_data():
    if 'user_id' in session:
        return jsonify({
            'user_id': session['user_id'],
            'email': session['email']
        }), 200
    else:
        return jsonify({'message': 'No active session found.'}), 401

@app.route('/addProduct', methods=['POST'])
def add_product():
    data = request.form
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')

    if not (name and description and price):
        return jsonify({'message': 'Missing required fields'}), 400

    try:
        product= Product(name,description,price)
        product.insertProduct()
        return jsonify({'message': 'Product added successfully','product_id':product.product_id}), 201
    except Exception as e:
        return jsonify({'message': f'Failed to add product: {str(e)}'}), 500

@app.route('/getAllProducts', methods=['GET'])
def getProducts():
    try:
        products = Product.getAllProducts()
        return jsonify({"message":"Success","products":products}),200
    except Exception as e:
        return jsonify({"message": "Error occurred", "error": str(e)}), 500

@app.route('/addCart', methods=['POST'])
def add_to_cart():
    data = request.form
    prod_id = data.get('product_id')
    user_id = data.get('user_id')

    if not (prod_id and user_id):
        return jsonify({'message': 'Missing required fields'}), 400

    try:
        cart= Cart(user_id,prod_id)
        cart.insertCart()
        return jsonify({'message': 'Product added to cart successfully','prod_cart_id':cart.id}), 201
    except Exception as e:
        return jsonify({'message': f'Failed to add product: {str(e)}'}), 500

@app.route('/getCart/<int:user_id>', methods=['GET'])
def getUserCart(user_id):
    try:
        cart = Cart.getCart(user_id)
        return jsonify({"message":"Success","cart":cart}),200
    except Exception as e:
        return jsonify({"message": "Error occurred", "error": str(e)}), 500

if __name__ == '__main__':
    app.run()