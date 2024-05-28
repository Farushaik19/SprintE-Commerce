from database import db
from datetime import datetime
class Product:
    def __init__(self, name, description, price, image_url, product_id=None, created_at=None, updated_at=None):
        self.product_id = product_id
        self.name = name
        self.description = description
        self.price = price
        self.imageurl = image_url
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()


    def insertProduct(self):
        cursor = db.cursor()
        sql = """
        INSERT INTO products (name, description, price, created_at, updated_at, imageurl)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        print("insert query is ",sql)
        cursor.execute(sql, (
            self.name,
            self.description,
            self.price,
            self.created_at,
            self.updated_at,
            self.imageurl
        ))
        self.product_id = cursor.lastrowid
        db.commit()

    @classmethod
    def getAllProducts(cls):
        cursor = db.cursor()
        sql = """
            SELECT * FROM products
        """
        cursor.execute(sql)
        products = cursor.fetchall()
        cursor.close()
        return products

    @classmethod
    def getProductbyId(cls,id):
        cursor = db.cursor()
        sql = f"""
                SELECT * FROM products where product_id = {id}
            """
        cursor.execute(sql)
        products = cursor.fetchall()
        cursor.close()
        return products[0]

    @classmethod
    def deleteProduct(cls, pid):
        cursor = db.cursor()
        sql = """
               DELETE FROM products WHERE product_id = %s;
           """
        cursor.execute(sql, (pid,))
        db.commit()
        cursor.close()

