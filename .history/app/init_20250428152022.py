from flask import Flask
import mysql.connector

def create_app():
    app = Flask(__name__)

    # Database Configuration
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'your_password'
    app.config['MYSQL_DATABASE'] = 'your_database_name'

    from app.routes import main
    app.register_blueprint(main)

    return app

def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='your_password',
        database='your_database_name'
    )
    return connection
