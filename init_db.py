import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()

MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
MYSQL_USER = os.getenv('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
MYSQL_DB = os.getenv('MYSQL_DB', 'food_delivery')

def create_database():
    try:
        connection = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD
        )
        cursor = connection.cursor()
        # Drop database if exists and recreate
        cursor.execute(f"DROP DATABASE IF EXISTS {MYSQL_DB}")
        cursor.execute(f"CREATE DATABASE {MYSQL_DB}")
        print(f"Database '{MYSQL_DB}' created successfully")
        cursor.close()
        connection.close()
        return True
    except Error as e:
        print(f"Error creating database: {e}")
        return False

def create_connection():
    try:
        connection = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def init_db():
    if not create_database():
        return
    
    connection = create_connection()
    if connection:
        cursor = None
        try:
            cursor = connection.cursor()
            
            # Read and execute the SQL schema file
            with open('schema.sql', 'r') as file:
                sql_script = file.read()
            
            # Split the script into individual statements and execute each
            statements = sql_script.split(';')
            for statement in statements:
                statement = statement.strip()
                if statement and not statement.startswith('--') and not statement.startswith('SET'):
                    try:
                        cursor.execute(statement)
                    except Error as e:
                        print(f"Warning: Could not execute statement: {e}")
            
            connection.commit()
            print("Database schema created successfully")
            cursor.close()
            connection.close()
        except Error as e:
            print(f"Error initializing database: {e}")
            if cursor:
                cursor.close()
            if connection.is_connected():
                connection.close()
    else:
        print("Failed to connect to database")

if __name__ == "__main__":
    init_db()