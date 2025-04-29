# app/routes.py

from flask import Blueprint, render_template, request
import numpy as np
import joblib
from app.db import get_db_connection

main = Blueprint('main', __name__)

model = joblib.load('models.pkl')

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        data = [float(x) for x in request.form.values()]
        final_features = np.array(data).reshape(1, -1)
        prediction = model.predict(final_features)[0]

        # Connect to MySQL
        db = get_db_connection()
        cursor = db.cursor()

        # Insert input features + prediction into database
        sql = "INSERT INTO predictions (feature1, feature2, feature3, feature4, feature5, feature6, feature7, feature8, prediction) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = tuple(data) + (int(prediction),)
        cursor.execute(sql, val)
        db.commit()

        cursor.close()
        db.close()

        return render_template('result.html', prediction=prediction)
