from database import db
from datetime import datetime
class Product:
    def __init__(self, name, description, price, product_id=None, created_at=None, updated_at=None):
        self.product_id = product_id
        self.name = name
        self.description = description
        self.price = price
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def insertProduct(self):
        cursor = db.cursor()
        sql = """
        INSERT INTO products (name, description, price, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s)
        """
        print("insert query is ",sql)
        cursor.execute(sql, (
            self.name,
            self.description,
            self.price,
            self.created_at,
            self.updated_at
        ))
        self.product_id = cursor.lastrowid
        db.commit()
        db.close()