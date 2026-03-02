"""
Model 2: Blood Glucose Estimation Model
Uses Gradient Boosting Classifier to estimate glucose ranges
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os

def train_glucose_model():
    """Train blood glucose estimation model"""
    print("=" * 60)
    print("Training Model 2: Blood Glucose Estimation")
    print("=" * 60)
    
    # Load training data
    df = pd.read_csv('data/training/glucose_train.csv')
    
    # Features and labels
    X = df[['age', 'bmi', 'meal_timing', 'activity_level']]
    y = df['glucose_range']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Train Gradient Boosting model
    model = GradientBoostingClassifier(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        random_state=42
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\nModel Accuracy: {accuracy:.4f}")
    print("\nClassification Report:")
    print(classification_report(
        y_test, y_pred,
        target_names=['Low', 'Normal', 'High']
    ))
    
    # Save model
    os.makedirs('models', exist_ok=True)
    joblib.dump(model, 'models/glucose_model.pkl')
    print("\n✅ Model saved to models/glucose_model.pkl")
    
    return model

if __name__ == '__main__':
    train_glucose_model()