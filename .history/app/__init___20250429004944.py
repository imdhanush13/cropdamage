from flask import Flask
import mysql.connector
import os
import os

def create_app():
    app = Flask(__name__)

    # Set the secret key to a random value
    app.config['SECRET_KEY'] = os.urandom(24)

    return app


def create_app():
    app = Flask(__name__)

    # (Optional) Database Configuration
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'Dhanush08@'
    app.config['MYSQL_DATABASE'] = 'cropdamagedb'

    from app.routes import main
    app.register_blueprint(main)

    return app

def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Dhanush08@',
        database='cropdamagedb'
    )
    return connection
