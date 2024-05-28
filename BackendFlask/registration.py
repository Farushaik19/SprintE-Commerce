from flask import Flask, request
from database import db
import pymysql
from flask import Flask, jsonify, session, redirect, url_for, flash
from flask_bcrypt import Bcrypt
import secrets
import re

app = Flask(__name__)

secret_key = secrets.token_hex(16)
app.secret_key = secret_key

cursor = db.cursor()
cursor.execute("USE Ecom")

# Closing the cursor and connection to the database
# cursor.close()
# db.close()

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

if __name__ == '__main__':
    app.run(port=8000)


