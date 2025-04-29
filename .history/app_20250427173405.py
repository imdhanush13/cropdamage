import pickle
from flask import Flask, request, jsonify, render_template
import mysql.connector

# Load your trained model
model = pickle.load(open('crop_damage_models.pkl', 'rb'))

app = Flask(__name__)

# Connect to MySQL Database
def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='your_password',  # Replace with your MySQL password
        database='your_database'  # Replace with your database name
    )
    return connection

@app.route('/')
def home():
    return render_template('index.html')  # The home route renders the index.html file

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()  # Get the data from the POST request

    # Extract features from the data (use the correct feature names from your model)
    features = [data['feature1'], data['feature2'], data['feature3'], data['feature4'], data['feature5'], data['feature6']]

    # Make prediction
    prediction = model.predict([features])

    # Save user data to database
    connection = get_db_connection()
    cursor = connection.cursor()

    # Assuming you're saving name, email, and features to the database
    cursor.execute("INSERT INTO users (name, email, feature1, feature2, feature3, feature4, feature5, feature6) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", 
                   (data['name'], data['email'], data['feature1'], data['feature2'], data['feature3'], data['feature4'], data['feature5'], data['feature6']))
    connection.commit()  # Commit the transaction
    cursor.close()

    # Return the prediction as a JSON response
    return jsonify({'prediction': prediction[0]})

if __name__ == "__main__":
    app.run(debug=True)
