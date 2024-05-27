from flask import Flask, request, jsonify
from database import db
from products import Product
from carts import Cart

app = Flask(__name__)


@app.route('/addProduct', methods=['POST'])
def add_product():
    # Extract product data from the request
    data = request.json
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')
    # Check if all required fields are present
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



if __name__ == '__main__':
    app.run()

