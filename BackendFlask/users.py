from database import db

def create_users_table():

    # Create a cursor object to execute SQL commands
    cursor = db.cursor()

    # SQL statement to create the users table
    create_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        email VARCHAR(255) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL
    )
    """

    try:
        # Execute the SQL command
        cursor.execute("USE Ecom")
        cursor.execute(create_table_query)
        # Commit the changes to the database
        db.commit()
        print("Users table created successfully.")
    except Exception as e:
        # Rollback in case of an error
        db.rollback()
        print("Error creating users table:", e)
    finally:
        # Close the cursor and database connection
        cursor.close()
        db.close()

if __name__ == "__main__":
    create_users_table()
