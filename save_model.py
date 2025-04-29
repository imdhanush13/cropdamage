# save_model.py

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
from sklearn.model_selection import train_test_split

# 1. Load the data
train = pd.read_csv('Crop_Damage_Train.csv')

# 2. Preprocess
train['Number_Weeks_Used'] = train['Number_Weeks_Used'].fillna(train['Number_Weeks_Used'].median())

X = train.drop(['ID', 'Crop_Damage'], axis=1)
y = train['Crop_Damage']

# 3. Train-Test Split (optional, but shows good practice)
x_train, x_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Train the model
model = RandomForestClassifier(random_state=42)
model.fit(x_train, y_train)

# 5. Save the model
joblib.dump(model, 'models.pkl')

print("✅ Model trained and saved as models.pkl!")
