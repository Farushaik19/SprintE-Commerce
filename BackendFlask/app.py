from flask import Flask, request
from database import db

app = Flask(__name__)


cursor = db.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS books_db")
cursor.execute("SHOW DATABASES")

for databases in cursor:
    print(databases)

# Closing the cursor and connection to the database
cursor.close()
db.close();