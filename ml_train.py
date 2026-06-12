# ml_train.py
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_absolute_error
import joblib
import os

# ==================== 1. Generate synthetic training data ====================
np.random.seed(42)
n_samples = 2000

data = {
    'previous_cgpa': np.random.uniform(4, 10, n_samples),
    'attendance': np.random.uniform(40, 100, n_samples),
    'assignment_submission_rate': np.random.uniform(30, 100, n_samples),
    'study_hours_per_day': np.random.uniform(0, 12, n_samples),
    'backlogs': np.random.poisson(0.5, n_samples),
    'family_income': np.random.choice([0,1,2,3], n_samples),  # 0=low,1=medium,2=high,3=very_high
    'high_school_percentage': np.random.uniform(50, 100, n_samples),
    'entrance_score': np.random.uniform(50, 200, n_samples),
}

df = pd.DataFrame(data)

# Generate target (final CGPA) based on a formula + noise
df['final_cgpa'] = (
    0.3 * df['previous_cgpa'] +
    0.2 * (df['attendance'] / 100 * 10) +
    0.15 * (df['assignment_submission_rate'] / 100 * 10) +
    0.1 * (df['study_hours_per_day'] / 12 * 10) +
    -0.1 * df['backlogs'] +
    0.05 * (df['high_school_percentage'] / 100 * 10) +
    0.05 * (df['entrance_score'] / 200 * 10) +
    np.random.normal(0, 0.3, n_samples)
).clip(0, 10)

# ==================== 2. Prepare features and target ====================
feature_cols = ['previous_cgpa', 'attendance', 'assignment_submission_rate',
                'study_hours_per_day', 'backlogs', 'family_income',
                'high_school_percentage', 'entrance_score']
X = df[feature_cols]
y = df['final_cgpa']

# Split into train and test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalise features (important for some models, but Random Forest doesn't strictly need it – still good practice)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ==================== 3. Train Random Forest ====================
rf = RandomForestRegressor(n_estimators=100, max_depth=10, min_samples_split=5,
                           random_state=42, n_jobs=-1)
rf.fit(X_train_scaled, y_train)

# ==================== 4. Evaluate ====================
y_pred = rf.predict(X_test_scaled)
r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
print(f"Model R² score: {r2:.4f}")
print(f"Mean Absolute Error: {mae:.4f}")

# ==================== 5. Save model and scaler ====================
os.makedirs('apps/ml_model/saved_models', exist_ok=True)
joblib.dump(rf, 'apps/ml_model/saved_models/rf_model.pkl')
joblib.dump(scaler, 'apps/ml_model/saved_models/scaler.pkl')
print("Model and scaler saved successfully.")