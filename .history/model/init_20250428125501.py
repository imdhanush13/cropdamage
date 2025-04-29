import pickle
from flask import Blueprint, request, jsonify
import mysql.connector
from sklearn.preprocessing import LabelEncoder

# Load the trained model and LabelEncoders
model = pickle.load(open('crop_damage_models.pkl', 'rb'))

# Create Blueprint
predict_blueprint = Blueprint('predict', __name__)

# Load LabelEncoders
crop_damage_encoder = LabelEncoder()
crop_damage_encoder.fit(['Minimal Damage', 'Partial Damage', 'Significant Damage'])

crop_type_encoder = LabelEncoder()
crop_type_encoder.fit(['Kharif', 'Rabi'])

soil_type_encoder = LabelEncoder()
soil_type_encoder.fit(['Alluvial', 'Black-Cotton'])

pesticide_encoder = LabelEncoder()
pesticide_encoder.fit(['Insecticides', 'Bactericides', 'Herbicides'])

season_encoder = LabelEncoder()
season_encoder.fit(['Summer', 'Monsoon', 'Winter'])

# Database connection function
def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='your_password',
        database='your_database'
    )
    return connection

# Predict function using the blueprint
@predict_blueprint.route('/', methods=['POST'])
def predict():
    data = request.get_json()  # Get data from the request

    # Extract and encode features
    crop_type = crop_type_encoder.transform([data['crop_type']])[0]
    soil_type = soil_type_encoder.transform([data['soil_type']])[0]
    pesticide_use = pesticide_encoder.transform([data['pesticide_use_category']])[0]
    season = season_encoder.transform([data['season']])[0]
    
    # Numerical features
    estimated_insects_count = data['estimated_insects_count']
    number_doses_week = data['number_doses_week']
    number_weeks_used = data['number_weeks_used']
    number_weeks_quit = data['number_weeks_quit']
    
    # Prepare features for prediction
    features = [estimated_insects_count, crop_type, soil_type, pesticide_use, number_doses_week, 
                number_weeks_used, number_weeks_quit, season]

    # Make prediction
    prediction = model.predict([features])

    # Decode the predicted value
    prediction_label = crop_damage_encoder.inverse_transform([prediction[0]])[0]

    # Save user data to database
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO users (name, email, predicted_crop_damage) VALUES (%s, %s, %s)", 
                   (data['name'], data['email'], prediction_label))
    connection.commit()
    cursor.close()

    return jsonify({'prediction': prediction_label})
