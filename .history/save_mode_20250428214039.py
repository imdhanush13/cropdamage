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
y = test['Crop_Damage']

from sklearn.model_selection import train_test_split, cross_val_score
x_train, x_test, y_train, y_test = train_test_split(x,y,test_size =0.2, random_state=42)
# 3. Train the model
model = RandomForestClassifier(random_state=42)
model.fit(x_train,y_train)


x_test_final = test.drop('ID',axis=1)
# 4. Save the model
joblib.dump(model, 'models.pkl')

print("✅ Model trained and saved as models.pkl!")
