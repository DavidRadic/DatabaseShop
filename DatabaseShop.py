import psycopg2
import Config  # Imports database

def connect_to_db():
    try:
        connection = psycopg2.connect(
            host=Config.DB_HOST,
            database=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            port=Config.DB_PORT
        )
        return connection
    except psycopg2.Error as e:
        print("Error connecting to the database:", e)
        return None

connection = connect_to_db()
if connection is None:
    exit()  # Close program if connection fails
cursor = connection.cursor()