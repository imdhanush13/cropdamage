# app/db.py

import mysql.connector

def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Dhanush08@',   # ✅ Correct password
        database='cropdamagedb'  # ✅ Correct database name
    )
    return connection
