from database import db
from products import Product
from carts import Cart
import secrets
import pymysql
from flask import Flask, jsonify, request, session, redirect, url_for, flash
from flask_bcrypt import Bcrypt
import re
import requests
import random

app = Flask(__name__)
frontEnd = "http://127.0.0.1:8000/"
secret_key = secrets.token_hex(16)
app.secret_key = secret_key

@app.route('/addProduct', methods=['POST'])
def add_product():
    # Extract product data from the request
    data = request.json
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')
    # Check if all required fields are present
    image_url = "https://images.unsplash.com/photo-1511556820780-d912e42b4980?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w2MTY4NjB8MHwxfHNlYXJjaHwxfHxwcm9kdWN0c3xlbnwwfHx8fDE3MTY4ODgyMTR8MA&ixlib=rb-4.0.3&q=80&w=1080"
    try:
        for i in range(2):
            response = requests.get(
                "https://api.unsplash.com/search/photos/?query=products&per_page=10&client_id=hgREOQ-PsXIYeyLu61Eu08GpwxvNhA2k8mlpWyBhiXU")
            data = response.json()
            image = random.choice(data['results'])
            image_url = image['urls']['regular']

    except Exception as e:
        print('No images found.', str(e))

    if not (name and description and price):
        return jsonify({'message': 'Missing required fields'}), 400

    try:
        product= Product(name,description,price,image_url)
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



#Add to Cart
@app.route('/addCart', methods=['POST'])
def add_to_cart():
    # Extract product data from the request

    data = request.get_json()

    prod_id = data.get('product_id')
    user_id = data.get('user_id')
    # Check if all required fields are present

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
@app.route('/getUserCartProducts/<int:user_id>', methods=['GET'])
def getUserCartProducts(user_id):
    try:
        userCart = Cart.getCart(user_id)
        cartProds = []
        for cart in userCart:
            cartProds.append(Product.getProductbyId(cart[2]))

        return jsonify({"message":"Success","cart":cartProds,"userId":user_id}),200
    except Exception as e:
        return jsonify({"message": "Error occurred", "error": str(e)}), 500



#USER REGISTRATION CODE

# Initialize Flask-Bcrypt
bcrypt = Bcrypt(app)

# Email validation function
def is_valid_email(email):
    # Regular expression for validating an email
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(regex, email)

#USER LOGIN
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

#user[0] is likely the user ID, user[1] is the user's email, and user[2] is the hashed password. 
    if user and bcrypt.check_password_hash(user[2], password):
        session['user_id'] = user[0]
        session['email'] = user[1]
        session['is_admin'] = user[3]
        return jsonify({'message': 'Login successful', 'user_id': user[0], 'email': user[1]})
    else:
        return jsonify({'message': 'Login unsuccessful. Please check email and password.'}), 401

#USER SIGNUP
@app.route('/signup', methods=['POST'])
def signup():
    email = request.json.get('email')
    password = request.json.get('password')
    print("data got is ",request.json)

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
        return jsonify({'message': 'User registered successfully'}), 201

#USER FORGOT PASSWORD
@app.route('/forgot_password', methods=['POST'])
def forgot_password():
    email = request.json.get('email')
    new_password = request.json.get('new_password')

    if not is_valid_email(email):
        return jsonify({'message': 'Invalid email format. Please enter a valid email address.'}), 400


    cur = db.cursor()
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cur.fetchone()

    if user:
        password_hash = bcrypt.generate_password_hash(new_password).decode('utf-8')
        cur.execute("UPDATE users SET password_hash = %s WHERE email = %s", (password_hash, email))
        db.commit()
        cur.close()
        return jsonify({'message': 'Password updated successfully.'}), 200
    else:
        return jsonify({'message': 'Email not found. Please enter a valid email address.'}), 404

#USER LOGOUT
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'You have been logged out.'}), 200

# deletion of product from cart
@app.route('/removeProduct/<int:prod_id>/<int:uid>', methods=['POST'])
def removeProduct(prod_id,uid):
    try:
        Cart.removeProdUser(prod_id,uid)
        return redirect(frontEnd+"cart")
    except Exception as e:
        print(str(e))
        return jsonify({'error': 'something went wrong during deletion'})

@app.route('/deleteProduct/<int:prod_id>', methods=['POST'])
def deleteProduct(prod_id):
    try:
        Product.deleteProduct(prod_id)
        return redirect(frontEnd)
    except Exception as e:
        print(str(e))
        return jsonify({'error': 'something went wrong during deletion'})




if __name__ == '__main__':
    app.run()

