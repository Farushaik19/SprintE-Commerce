from flask import Flask, render_template, request, redirect
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

@app.route('/cart')
def cart():
   return render_template('cartpage.html')

@app.route('/login')
def login():
   return render_template('login.html')
@app.route('/signIn')
def signup():
   return render_template('signIn.html')
@app.route('/forgotPassword')
def forgotPassword():
   return render_template('forgotPassword.html')

@app.route('/addCart',methods=['POST'])
def addTocart():
   print("data is ",request.form["product_id"])
   res = requests.post("http://127.0.0.1:5000/addCart",
                            json={"product_id": request.form["product_id"],
                                  "user_id": request.form["user_id"]
                                  },
                            headers={"Content-Type": "application/json"},
                            )
   if res.status_code == 201:
       return redirect("http://127.0.0.1:8000")
   else:
       return redirect("http://127.0.0.1:8000")

# Add Product Post
@app.route('/addProduct',methods=["POST"])
def addProduct():

    res = requests.post("http://127.0.0.1:5000/addProduct",
                        json={"name": request.form["name"],
                              "description": request.form["desc"],
                              "price": request.form["price"],
                              },
                        headers={"Content-Type": "application/json"},
                        )
    if res.status_code == 201:
        return redirect("http://127.0.0.1:8000")
    else:
        return redirect("http://127.0.0.1:8000")


if __name__ == '__main__':
   app.run(port=8000)