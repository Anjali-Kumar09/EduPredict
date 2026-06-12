# apps/ml_model/predictor.py
import joblib
import numpy as np
import os
from django.conf import settings

class PerformancePredictor:
    def __init__(self):
        model_path = os.path.join(settings.BASE_DIR, 'apps/ml_model/saved_models/rf_model.pkl')
        scaler_path = os.path.join(settings.BASE_DIR, 'apps/ml_model/saved_models/scaler.pkl')
        self.model = joblib.load(model_path)
        self.scaler = joblib.load(scaler_path)
        self.feature_cols = ['previous_cgpa', 'attendance', 'assignment_submission_rate',
                             'study_hours_per_day', 'backlogs', 'family_income',
                             'high_school_percentage', 'entrance_score']

    def predict(self, features_dict):
        # features_dict must contain all keys in feature_cols
        input_array = np.array([features_dict[col] for col in self.feature_cols]).reshape(1, -1)
        scaled = self.scaler.transform(input_array)
        pred = self.model.predict(scaled)[0]
        # risk levels
        if pred >= 8.0:
            risk = 'Low'
        elif pred >= 5.0:
            risk = 'Medium'
        else:
            risk = 'High'
        return {
            'predicted_cgpa': round(pred, 2),
            'risk_level': risk,
            'confidence': round(np.std([tree.predict(scaled)[0] for tree in self.model.estimators_]) * 10, 2)
        }

predictor = PerformancePredictor()