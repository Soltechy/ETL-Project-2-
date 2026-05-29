import psycopg2
from dotenv import load_dotenv
import os
import logging


load_dotenv()

def create_connection():
    connection = None
    try:
        connection = psycopg2.connect(
            database= os.getenv("DB_NAME"),
            user= os.getenv("DB_USER"),
            password= os.getenv("DB_PASSWORD"),
            host= os.getenv("DB_HOST"),
            port= os.getenv("DB_PORT"),
        )
        print("Connection to PostgreSQL DB successful")
    except Exception as e:
        print(f"The error '{e}' occurred")
    return connection


def insert_data(connection, df):
    try:
        cursor = connection.cursor()
        for _, row in df.iterrows():
            print(f"inserting data - {row}")
            cursor.execute("""
                INSERT INTO gasleet_data VALUES (%s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s)
            """, tuple(row))
        connection.commit()
        cursor.close()
        connection.close()

        logging.info("Data inserted successfully")
        return True
    except Exception as e:
        print(f"The error '{e}' occurred")
        return False