import pickle
from flask import Flask, request, jsonify
import mysql.connector

# Load your trained model
model = pickle.load(open('crop_damage_models.pkl', 'rb'))

app = Flask(__name__)

# Connect to MySQL Database
def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='your_password',
        database='your_database'
    )
    return connection

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()  # Get the data from the request

    # Extract features from the data
    features = [data['feature1'], data['feature2'], data['feature3'], ...]

    # Make prediction
    prediction = model.predict([features])

    # Save user data to database
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (data['name'], data['email']))
    connection.commit()
    cursor.close()

    return jsonify({'prediction': prediction[0]})

if __name__ == "__main__":
    app.run(debug=True)
