"""
Model 4: Speech Pattern Analysis
Uses Logistic Regression to analyze speech patterns
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.pipeline import Pipeline
import joblib
import os

def train_speech_model():
    """Train speech pattern analysis model"""
    print("=" * 60)
    print("Training Model 4: Speech Pattern Analysis")
    print("=" * 60)
    
    # Load training data
    df = pd.read_csv('data/training/speech_train.csv')
    
    # Features and labels
    X = df[['speech_rate', 'pause_frequency', 'pitch_variability']]
    y = df['label']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Create pipeline with scaling and Logistic Regression
    model = Pipeline([
        ('scaler', StandardScaler()),
        ('logreg', LogisticRegression(
            multi_class='multinomial',
            solver='lbfgs',
            max_iter=1000,
            random_state=42
        ))
    ])
    
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\nModel Accuracy: {accuracy:.4f}")
    print("\nClassification Report:")
    print(classification_report(
        y_test, y_pred,
        target_names=['Normal', 'Slurred/Slow', 'Stressed']
    ))
    
    # Save model
    os.makedirs('models', exist_ok=True)
    joblib.dump(model, 'models/speech_model.pkl')
    print("\n✅ Model saved to models/speech_model.pkl")
    
    return model

if __name__ == '__main__':
    train_speech_model()