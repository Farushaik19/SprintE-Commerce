from database import db
from datetime import datetime

class Cart:
    def __init__(self, user_id, product_id,id=None,created_at=None,updated_at=None):
        self.id = id
        self.user_id = user_id
        self.product_id = product_id
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()


    def insertCart(self):
        cursor = db.cursor()
        sql = """
        INSERT INTO carts (user_id, product_id, created_at, updated_at)
        VALUES (%s, %s, %s, %s)
        """
        print("insert query is ",sql)
        cursor.execute(sql, (
            self.user_id,
            self.product_id,
            self.created_at,
            self.updated_at
        ))
        self.id = cursor.lastrowid
        db.commit()

    @classmethod
    def getCart(cls,user_id):
        cursor = db.cursor()
        sql = f"""
        SELECT * FROM carts WHERE user_id = {user_id}
        """
        cursor.execute(sql)
        cart = cursor.fetchall()
        cursor.close()
        return cart
