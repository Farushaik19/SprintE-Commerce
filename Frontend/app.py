from flask import Flask, render_template
import requests
app = Flask(__name__)

@app.route('/')
def home():
   response = requests.get('http://localhost:5000/getAllProducts')
   if response.status_code == 200:
      products = response.json()# Convert the response to JSON
   else:
      products = {'products':[]}  # Handle the case where the request fails
   print("products are ",products)
   return render_template('homepage.html', products=products['products'])
@app.route('/login')
def login():
   return render_template('login.html')

@app.route('/cart')
def cart():
   return render_template('cartpage.html')

if __name__ == '__main__':
   app.run(port=8000)
