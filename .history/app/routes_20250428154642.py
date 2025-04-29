from flask import Blueprint, render_template, request, jsonify
import pickle
from app import get_db_connection

main = Blueprint('main', __name__)

# Load your trained model
model = pickle.load(open('crop_damage_models.pkl', 'rb'))

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
        
        estimated_insects_count = int(request.form['Estimated_Insects_Count'])
        crop_type = 1 if request.form['Crop_Type'] == 'Rabi' else 0  # Convert to 1 for Rabi, 0 for Kharif
        soil_type = 1 if request.form['Soil_Type'] == 'Black-Cotton' else 0  # 1 for Black-Cotton, 0 for Alluvial
        pesticide_use_category = {'Insecticides': 1, 'Bactericides': 2, 'Herbicides': 3}[request.form['Pesticide_Use_Category']]
        number_doses_week = int(request.form['Number_Doses_Week'])
        number_weeks_used = float(request.form['Number_Weeks_Used'])
        number_weeks_quit = int(request.form['Number_Weeks_Quit'])
        season = {'Summer': 1, 'Monsoon': 2, 'Winter': 3}[request.form['Season']]

        features = [
            estimated_insects_count,
            crop_type,
            soil_type,
            pesticide_use_category,
            number_doses_week,
            number_weeks_used,
            number_weeks_quit,
            season
        ]

        # Predict using the model
        prediction = model.predict([features])[0]
        
        # Map the model output to the corresponding label
        label_mapping = {
            0: "Minimal Damage",
            1: "Partial Damage",
            2: "Significant Damage"
        }
        
        predicted_crop_damage = label_mapping.get(prediction, "Unknown")

        # Render the template with the prediction
        return render_template('index.html', prediction_text=f'Predicted Crop Damage: {predicted_crop_damage}')


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
