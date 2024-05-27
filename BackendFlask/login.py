from flask import Flask, request
from database import db
from flask import Flask, jsonify, request, session, redirect, url_for, flash
from flask_bcrypt import Bcrypt

cursor = db.cursor()
# Initialize Flask-Bcrypt
bcrypt = Bcrypt(app)

#USER LOGIN
@app.route('/login', methods=['GET','POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    cur = db.cursor()
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cur.fetchone()
    cur.close()

#user[0] is the user ID, user[1] is the user's email, and user[2] is the hashed password. 
    if user and bcrypt.check_password_hash(user[2], password):
        user_id = user[0]
        email = user[1]
        return jsonify({'message': 'Login successful', 'user_id': user_id, 'email': email})
    else:
        return jsonify({'message': 'Login unsuccessful. Please check email and password.'}), 401
