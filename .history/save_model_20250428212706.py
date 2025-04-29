# save_model.py
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Load your dataset
data = pd.read_csv('Crop_Damage_Train.csv')

# Fill missing values
data['Number_Weeks_Used'] = data['Number_Weeks_Used'].fillna(data['Number_Weeks_Used'].median())

# Features and Target
X = data.drop(['ID', 'Crop_Damage'], axis=1)
y = data['Crop_Damage']

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save the model
joblib.dump(model, 'app/model.pkl')

print("✅ Model trained and saved as 'app/model.pkl'")
