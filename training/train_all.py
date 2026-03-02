"""
Master Training Script
Trains all six RehabSense AI models
"""

import sys
import os

# Add training directory to path
sys.path.append(os.path.dirname(__file__))

from train_heartbeat import train_heartbeat_model
from train_glucose import train_glucose_model
from train_breathing import train_breathing_model
from train_speech import train_speech_model
from train_emotion import train_emotion_model
from train_posture import train_posture_model

def train_all_models():
    """Train all six models sequentially"""
    print("\n" + "=" * 60)
    print("REHABSENSE MODEL TRAINING")
    print("=" * 60)
    print("\nTraining all six AI models...\n")
    
    try:
        # Model 1: Heartbeat
        train_heartbeat_model()
        print("\n")
        
        # Model 2: Glucose
        train_glucose_model()
        print("\n")
        
        # Model 3: Breathing
        train_breathing_model()
        print("\n")
        
        # Model 4: Speech
        train_speech_model()
        print("\n")
        
        # Model 5: Emotion
        train_emotion_model()
        print("\n")
        
        # Model 6: Posture
        train_posture_model()
        print("\n")
        
        print("=" * 60)
        print("✅ ALL MODELS TRAINED SUCCESSFULLY!")
        print("=" * 60)
        print("\nTrained models saved in models/ directory:")
        print("  - heartbeat_model.pkl")
        print("  - glucose_model.pkl")
        print("  - breathing_model.pkl")
        print("  - speech_model.pkl")
        print("  - emotion_model.pkl")
        print("  - posture_model.pkl")
        print("\nYou can now run the web application!")
        
    except Exception as e:
        print(f"\n❌ Error during training: {e}")
        raise

if __name__ == '__main__':
    train_all_models()