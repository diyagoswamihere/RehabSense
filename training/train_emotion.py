"""
Model 5: Emotional State Detection
Uses K-Nearest Neighbors to detect emotional states
"""

import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.pipeline import Pipeline
import joblib
import os

def train_emotion_model():
    """Train emotional state detection model"""
    print("=" * 60)
    print("Training Model 5: Emotional State Detection")
    print("=" * 60)
    
    # Load training data
    df = pd.read_csv('data/training/emotion_train.csv')
    
    # Features and labels
    X = df[['text_sentiment', 'voice_emotion', 'facial_emotion']]
    y = df['label']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Create pipeline with scaling and KNN
    model = Pipeline([
        ('scaler', StandardScaler()),
        ('knn', KNeighborsClassifier(
            n_neighbors=7,
            weights='distance',
            metric='euclidean'
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
        target_names=['Happy', 'Neutral', 'Stressed', 'Sad']
    ))
    
    # Save model
    os.makedirs('models', exist_ok=True)
    joblib.dump(model, 'models/emotion_model.pkl')
    print("\n✅ Model saved to models/emotion_model.pkl")
    
    return model

if __name__ == '__main__':
    train_emotion_model()