"""
Model 3: Breathing Irregularity Detection
Uses Support Vector Machine to detect breathing irregularities
"""

import pandas as pd
import numpy as np
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.pipeline import Pipeline
import joblib
import os

def train_breathing_model():
    """Train breathing irregularity detection model"""
    print("=" * 60)
    print("Training Model 3: Breathing Irregularity Detection")
    print("=" * 60)
    
    # Load training data
    df = pd.read_csv('data/training/breathing_train.csv')
    
    # Features and labels
    X = df[['breathing_rate', 'breath_depth', 'rest_vs_exercise']]
    y = df['label']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Create pipeline with scaling and SVM
    model = Pipeline([
        ('scaler', StandardScaler()),
        ('svm', SVC(kernel='rbf', C=1.0, gamma='scale', random_state=42))
    ])
    
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\nModel Accuracy: {accuracy:.4f}")
    print("\nClassification Report:")
    print(classification_report(
        y_test, y_pred,
        target_names=['Normal', 'Shallow', 'Irregular', 'Apnea Risk']
    ))
    
    # Save model
    os.makedirs('models', exist_ok=True)
    joblib.dump(model, 'models/breathing_model.pkl')
    print("\n✅ Model saved to models/breathing_model.pkl")
    
    return model

if __name__ == '__main__':
    train_breathing_model()