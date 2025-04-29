# app/routes.py

from flask import Flask, request, render_template
import pickle
import numpy as np

app = Flask(__name__)

# Load the model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

# Encoding functions for categorical variables
def encode_crop_type(crop_type):
    mapping = {'Rabi': 0, 'Kharif': 1}
    return mapping.get(crop_type, 0)

def encode_soil_type(soil_type):
    mapping = {'Alluvial': 0, 'Black-Cotton': 1}
    return mapping.get(soil_type, 0)

def encode_pesticide_use(pesticide_use):
    mapping = {'Insecticides': 1, 'Herbicides': 1, 'Herbicides': 2}
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
