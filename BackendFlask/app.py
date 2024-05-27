from flask import Flask, request
from database import db

app = Flask(__name__)


cursor = db.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS books_db")
cursor.execute("SHOW DATABASES")

for databases in cursor:
    print(databases)


#USER LOGOUT
@app.route('/logout', methods=['GET','POST'])
def logout():
    # session.clear()
    return jsonify({'message': 'You have been logged out.'}), 200

if __name__ == '__main__':
    app.run(debug=True)

# Closing the cursor and connection to the database
cursor.close()
db.close();
