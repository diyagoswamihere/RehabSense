"""
Model 6: Real-Time Posture Detection
Uses Decision Tree Classifier to detect posture issues
"""

import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os

def train_posture_model():
    """Train posture detection model"""
    print("=" * 60)
    print("Training Model 6: Real-Time Posture Detection")
    print("=" * 60)
    
    # Load training data
    df = pd.read_csv('data/training/posture_train.csv')
    
    # Features and labels
    X = df[['head_tilt', 'shoulder_alignment', 'spine_angle']]
    y = df['label']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Train Decision Tree model
    model = DecisionTreeClassifier(
        max_depth=8,
        min_samples_split=10,
        min_samples_leaf=5,
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
        target_names=['Good Posture', 'Forward Head', 'Slouched']
    ))
    
    # Save model
    os.makedirs('models', exist_ok=True)
    joblib.dump(model, 'models/posture_model.pkl')
    print("\n✅ Model saved to models/posture_model.pkl")
    
    return model

if __name__ == '__main__':
    train_posture_model()