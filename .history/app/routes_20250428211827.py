# app/routes.py

from flask import Flask, request, render_template
import pickle
import numpy as np

app = Flask(__name__)

# Load the model
with open('models.pkl', 'rb') as f:
    model = pickle.load(f)

# Encoding functions for categorical variables
def encode_crop_type(crop_type):
    mapping = {'Rabi': 0, 'Kharif': 1}
    return mapping.get(crop_type, 0)

def encode_soil_type(soil_type):
    mapping = {'Alluvial': 0, 'Black-Cotton': 1}
    return mapping.get(soil_type, 0)

def encode_pesticide_use(pesticide_use):
    mapping = {'Insecticides': 1, 'Herbicides': 2, 'Bactericides': 3}
    return mapping.get(pesticide_use, 0)

def encode_season(season):
    mapping = {'Summer': 1, 'Monsoon': 2, 'Winter': 3}
    return mapping.get(season, 0)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Fetch form data
        name = request.form['name']
        email = request.form['email']

        Estimated_Insects_Count = float(request.form['Estimated_Insects_Count'])
        Crop_Type = encode_crop_type(request.form['Crop_Type'])
        Soil_Type = encode_soil_type(request.form['Soil_Type'])
        Pesticide_Use_Category = encode_pesticide_use(request.form['Pesticide_Use_Category'])
        Number_Doses_Week = float(request.form['Number_Doses_Week'])
        Number_Weeks_Used = float(request.form['Number_Weeks_Used'])
        Number_Weeks_Quit = float(request.form['Number_Weeks_Quit'])
        Season = encode_season(request.form['Season'])

        # Prepare feature array
        features = np.array([[Estimated_Insects_Count, Crop_Type, Soil_Type, Pesticide_Use_Category,
                              Number_Doses_Week, Number_Weeks_Used, Number_Weeks_Quit, Season]])

        # Prediction
        prediction = model.predict(features)
        predicted_crop_damage = prediction[0]

        # Map prediction back to readable label (optional)
        crop_damage_mapping = {0: 'Minimal Damage', 1: 'Partial Damage', 2: 'Significant Damage'}
        readable_prediction = crop_damage_mapping.get(predicted_crop_damage, 'Unknown')

        return render_template('index.html', prediction_text=f'Predicted Crop Damage: {readable_prediction}')

if __name__ == '__main__':
    app.run(debug=True)
# app/routes.py
from flask import Flask, request, render_template
import joblib
import numpy as np

app = Flask(__name__)

# Load the model (ONLY ONCE here)
model = joblib.load('app/model.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Fetching form data
        estimated_insects_count = int(request.form['Estimated_Insects_Count'])
        crop_type = request.form['Crop_Type']
        soil_type = request.form['Soil_Type']
        pesticide_use_category = request.form['Pesticide_Use_Category']
        number_doses_week = int(request.form['Number_Doses_Week'])
        number_weeks_used = float(request.form['Number_Weeks_Used'])
        number_weeks_quit = int(request.form['Number_Weeks_Quit'])
        season = request.form['Season']

        # Encoding categorical values manually (important!!)
        crop_type_mapping = {'Rabi': 0, 'Kharif': 1}
        soil_type_mapping = {'Alluvial': 0, 'Black-Cotton': 1}
        pesticide_use_mapping = {'Insecticides': 0, 'Herbicides;Bactericides': 1, 'Herbicides': 2}
        season_mapping = {'Summer': 0, 'Monsoon': 1, 'Winter': 2}

        crop_type_encoded = crop_type_mapping[crop_type]
        soil_type_encoded = soil_type_mapping[soil_type]
        pesticide_use_encoded = pesticide_use_mapping[pesticide_use_category]
        season_encoded = season_mapping[season]

        # Arrange input features in same order used during training
        features = np.array([
            estimated_insects_count,
            crop_type_encoded,
            soil_type_encoded,
            pesticide_use_encoded,
            number_doses_week,
            number_weeks_used,
            number_weeks_quit,
            season_encoded
        ]).reshape(1, -1)

        # Predict
        prediction = model.predict(features)[0]

        # Map prediction to readable output
        crop_damage_mapping = {
            0: 'Minimal Damage',
            1: 'Partial Damage',
            2: 'Significant Damage'
        }

        predicted_crop_damage = crop_damage_mapping[prediction]

        return render_template('index.html', prediction_text=f'Predicted Crop Damage: {predicted_crop_damage}')

if __name__ == '__main__':
    app.run(debug=True)
