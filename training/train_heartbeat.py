"""
Model 1: Heartbeat Abnormality Detector
Uses Random Forest Classifier to detect heartbeat abnormalities
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os

def train_heartbeat_model():
    """Train heartbeat abnormality detection model"""
    print("=" * 60)
    print("Training Model 1: Heartbeat Abnormality Detector")
    print("=" * 60)
    
    # Load training data
    df = pd.read_csv('data/training/heartbeat_train.csv')
    
    # Features and labels
    X = df[['heart_rate', 'rr_interval_variance']]
    y = df['label']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Train Random Forest model
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        class_weight='balanced'
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\nModel Accuracy: {accuracy:.4f}")
    print("\nClassification Report:")
    print(classification_report(
        y_test, y_pred,
        target_names=['Normal', 'Bradycardia', 'Tachycardia', 'Irregular']
    ))
    
    # Save model
    os.makedirs('models', exist_ok=True)
    joblib.dump(model, 'models/heartbeat_model.pkl')
    print("\n✅ Model saved to models/heartbeat_model.pkl")
    
    return model

if __name__ == '__main__':
    train_heartbeat_model()