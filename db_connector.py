import mysql.connector
from mysql.connector import Error

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'mvc_db'
}

def get_db_connection():
    """Establishes and returns a database connection."""
    try:
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            # print('Connected to MySQL database')
            return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None