# save_model.py

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# 1. Load the data
train = pd.read_csv('Crop_Damage_Train.csv')
test = pd.read_csv('Crop_Damage_Test.csv')

# 2. Preprocess
train['Number_Weeks_Used'] = train['Number_Weeks_Used'].fillna(train['Number_Weeks_Used'].median())
test['Number_Weeks_Used'] = test['Number_Weeks_Used'].fillna(test['Number_Weeks_Used'].median())


X = train.drop(['ID', 'Crop_Damage'], axis=1)
y = data['Crop_Damage']

# 3. Train the model
model = RandomForestClassifier(random_state=42)
model.fit(X, y)

# 4. Save the model
joblib.dump(model, 'models.pkl')

print("✅ Model trained and saved as models.pkl!")
