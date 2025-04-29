from flask import Flask, render_template, request, redirect, url_for, session, Bl
import joblib
import numpy as np
from app import get_db_connection

main = Blueprint('main', __name__)
main.secret_key = 'your_secret_key'  # Replace with a secure key

# Load your trained model
model = joblib.load('models.pkl')

@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Store name and email in session
        session['name'] = request.form['name']
        session['email'] = request.form['email']
        return redirect(url_for('details'))
    return render_template('index.html')

@main.route('/details', methods=['GET', 'POST'])
def details():
    if request.method == 'POST':
        # Retrieve data from form
        estimated_insects_count = int(request.form['Estimated_Insects_Count'])
        crop_type = request.form['Crop_Type']
        soil_type = request.form['Soil_Type']
        pesticide_use_category = request.form['Pesticide_Use_Category']
        number_doses_week = int(request.form['Number_Doses_Week'])
        number_weeks_used = float(request.form['Number_Weeks_Used'])
        number_weeks_quit = int(request.form['Number_Weeks_Quit'])
        season = request.form['Season']

        # Encode categorical variables
        crop_type_mapping = {'Rabi': 0, 'Kharif': 1}
        soil_type_mapping = {'Alluvial': 0, 'Black-Cotton': 1}
        pesticide_use_mapping = {'Insecticides': 1, 'Herbicides': 2, 'Bactericides': 3}
        season_mapping = {'Summer': 1, 'Monsoon': 2, 'Winter': 3}

        crop_type_encoded = crop_type_mapping[crop_type]
        soil_type_encoded = soil_type_mapping[soil_type]
        pesticide_use_encoded = pesticide_use_mapping[pesticide_use_category]
        season_encoded = season_mapping[season]

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

        # Retrieve name and email from session
        name = session.get('name')
        email = session.get('email')

        # Store into MySQL database
        connection = get_db_connection()
        cursor = connection.cursor()
        sql = """
            INSERT INTO predictions (name, email, estimated_insects_count, crop_type, soil_type, pesticide_use_category,
                                      number_doses_week, number_weeks_used, number_weeks_quit, season, predicted_damage)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        val = (
            name,
            email,
            estimated_insects_count,
            crop_type,
            soil_type,
            pesticide_use_category,
            number_doses_week,
            number_weeks_used,
            number_weeks_quit,
            season,
            predicted_crop_damage
        )
        cursor.execute(sql, val)
        connection.commit()
        cursor.close()
        connection.close()

        return render_template('result.html', prediction_text=f'Predicted Crop Damage: {predicted_crop_damage}')
    return render_template('details.html')
