from flask import Blueprint, render_template, request, jsonify
import pickle
from routes import get_db_connection

main = Blueprint('main', __name__)

# Load your trained model
model = pickle.load(open('app/model.pkl', 'rb'))

# Mapping
crop_damage_mapping = {0: 'Minimal Damage', 1: 'Partial Damage', 2: 'Significant Damage'}
crop_type_mapping = {'Kharif': 1, 'Rabi': 0}
soil_type_mapping = {'Alluvial': 0, 'Black-Cotton': 1}
pesticide_use_mapping = {'Insecticides': 1, 'Bactericides': 3, 'Herbicides': 2}
season_mapping = {'Summer': 1, 'Monsoon': 2, 'Winter': 3}

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        Estimated_Insects_Count = int(request.form['Estimated_Insects_Count'])
        Crop_Type = crop_type_mapping[request.form['Crop_Type']]
        Soil_Type = soil_type_mapping[request.form['Soil_Type']]
        Pesticide_Use_Category = pesticide_use_mapping[request.form['Pesticide_Use_Category']]
        Number_Doses_Week = int(request.form['Number_Doses_Week'])
        Number_Weeks_Used = float(request.form['Number_Weeks_Used'])
        Number_Weeks_Quit = int(request.form['Number_Weeks_Quit'])
        Season = season_mapping[request.form['Season']]

        features = [
            Estimated_Insects_Count,
            Crop_Type,
            Soil_Type,
            Pesticide_Use_Category,
            Number_Doses_Week,
            Number_Weeks_Used,
            Number_Weeks_Quit,
            Season
        ]

        prediction = model.predict([features])[0]
        predicted_crop_damage = crop_damage_mapping[prediction]

        # Save to database
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (name, email, predicted_crop_damage) VALUES (%s, %s, %s)",
                       (name, email, predicted_crop_damage))
        connection.commit()
        cursor.close()
        connection.close()

        return render_template('index.html', prediction_text=f'Predicted Crop Damage: {predicted_crop_damage}')
