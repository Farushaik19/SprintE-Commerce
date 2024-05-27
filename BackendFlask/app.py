from flask import Flask, request, jsonify
from database import db
from products import Product
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


if __name__ == '__main__':
    app.run()

