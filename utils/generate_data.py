"""
Data Generation Script for RehabSense
Generates synthetic patient data for all six AI models
"""

import numpy as np
import pandas as pd
import json
import os
from datetime import datetime, timedelta

np.random.seed(42)

def generate_heartbeat_data(n_samples=1000, patient_type='normal'):
    """Generate ECG/heartbeat data"""
    if patient_type == 'normal':
        heart_rate = np.random.normal(75, 8, n_samples)
        rr_interval_variance = np.random.normal(0.05, 0.01, n_samples)
        label = np.random.choice([0, 1, 2, 3], n_samples, p=[0.8, 0.1, 0.05, 0.05])
    elif patient_type == 'improving':
        # Patient showing improvement over time
        heart_rate = np.concatenate([
            np.random.normal(95, 10, n_samples//2),  # Initially high
            np.random.normal(78, 8, n_samples//2)    # Improving
        ])
        rr_interval_variance = np.concatenate([
            np.random.normal(0.08, 0.02, n_samples//2),
            np.random.normal(0.05, 0.01, n_samples//2)
        ])
        label = np.concatenate([
            np.random.choice([1, 2, 3], n_samples//2, p=[0.4, 0.4, 0.2]),
            np.random.choice([0, 1], n_samples//2, p=[0.7, 0.3])
        ])
    
    return pd.DataFrame({
        'heart_rate': np.clip(heart_rate, 40, 180),
        'rr_interval_variance': np.clip(rr_interval_variance, 0.01, 0.15),
        'label': label  # 0: Normal, 1: Bradycardia, 2: Tachycardia, 3: Irregular
    })

def generate_glucose_data(n_samples=1000, patient_type='normal'):
    """Generate blood glucose estimation data"""
    age = np.random.randint(25, 75, n_samples)
    bmi = np.random.normal(25, 4, n_samples)
    meal_timing = np.random.choice([0, 1, 2, 3], n_samples)  # 0: Fasting, 1: Post-meal, 2: Pre-meal, 3: Random
    activity_level = np.random.choice([0, 1, 2], n_samples)  # 0: Low, 1: Moderate, 2: High
    
    if patient_type == 'improving':
        # Show improvement in glucose control
        glucose_range = np.concatenate([
            np.random.choice([0, 1, 2], n_samples//2, p=[0.2, 0.3, 0.5]),  # Initially poor
            np.random.choice([0, 1, 2], n_samples//2, p=[0.1, 0.7, 0.2])   # Improving
        ])
    else:
        glucose_range = np.random.choice([0, 1, 2], n_samples, p=[0.15, 0.7, 0.15])
    
    return pd.DataFrame({
        'age': age,
        'bmi': np.clip(bmi, 18, 40),
        'meal_timing': meal_timing,
        'activity_level': activity_level,
        'glucose_range': glucose_range  # 0: Low, 1: Normal, 2: High
    })

def generate_breathing_data(n_samples=1000, patient_type='normal'):
    """Generate breathing pattern data"""
    breathing_rate = np.random.normal(16, 3, n_samples)
    breath_depth = np.random.normal(0.5, 0.1, n_samples)
    rest_vs_exercise = np.random.choice([0, 1], n_samples, p=[0.7, 0.3])
    
    if patient_type == 'improving':
        label = np.concatenate([
            np.random.choice([0, 1, 2, 3], n_samples//2, p=[0.4, 0.3, 0.2, 0.1]),
            np.random.choice([0, 1], n_samples//2, p=[0.8, 0.2])
        ])
    else:
        label = np.random.choice([0, 1, 2, 3], n_samples, p=[0.7, 0.15, 0.1, 0.05])
    
    return pd.DataFrame({
        'breathing_rate': np.clip(breathing_rate, 8, 30),
        'breath_depth': np.clip(breath_depth, 0.2, 1.0),
        'rest_vs_exercise': rest_vs_exercise,
        'label': label  # 0: Normal, 1: Shallow, 2: Irregular, 3: Apnea risk
    })

def generate_speech_data(n_samples=1000, patient_type='normal'):
    """Generate speech pattern data (simulated features)"""
    speech_rate = np.random.normal(150, 20, n_samples)  # words per minute
    pause_frequency = np.random.normal(0.15, 0.05, n_samples)
    pitch_variability = np.random.normal(0.3, 0.1, n_samples)
    
    if patient_type == 'improving':
        label = np.concatenate([
            np.random.choice([0, 1, 2], n_samples//2, p=[0.3, 0.5, 0.2]),
            np.random.choice([0, 1], n_samples//2, p=[0.8, 0.2])
        ])
    else:
        label = np.random.choice([0, 1, 2], n_samples, p=[0.75, 0.15, 0.1])
    
    return pd.DataFrame({
        'speech_rate': np.clip(speech_rate, 80, 220),
        'pause_frequency': np.clip(pause_frequency, 0.05, 0.4),
        'pitch_variability': np.clip(pitch_variability, 0.1, 0.6),
        'label': label  # 0: Normal, 1: Slurred/Slow, 2: Stressed
    })

def generate_emotion_data(n_samples=1000, patient_type='normal'):
    """Generate emotional state data"""
    text_sentiment = np.random.normal(0.5, 0.2, n_samples)
    voice_emotion = np.random.normal(0.5, 0.2, n_samples)
    facial_emotion = np.random.normal(0.5, 0.2, n_samples)
    
    if patient_type == 'improving':
        label = np.concatenate([
            np.random.choice([0, 1, 2, 3], n_samples//2, p=[0.2, 0.2, 0.4, 0.2]),
            np.random.choice([0, 1, 2], n_samples//2, p=[0.5, 0.4, 0.1])
        ])
    else:
        label = np.random.choice([0, 1, 2, 3], n_samples, p=[0.4, 0.35, 0.15, 0.1])
    
    return pd.DataFrame({
        'text_sentiment': np.clip(text_sentiment, 0, 1),
        'voice_emotion': np.clip(voice_emotion, 0, 1),
        'facial_emotion': np.clip(facial_emotion, 0, 1),
        'label': label  # 0: Happy, 1: Neutral, 2: Stressed, 3: Sad
    })

def generate_posture_data(n_samples=1000, patient_type='normal'):
    """Generate posture detection data (simulated keypoints)"""
    # Simulated body keypoint features
    head_tilt = np.random.normal(0, 10, n_samples)
    shoulder_alignment = np.random.normal(0, 8, n_samples)
    spine_angle = np.random.normal(90, 15, n_samples)
    
    if patient_type == 'improving':
        label = np.concatenate([
            np.random.choice([0, 1, 2], n_samples//2, p=[0.3, 0.4, 0.3]),
            np.random.choice([0, 1], n_samples//2, p=[0.7, 0.3])
        ])
    else:
        label = np.random.choice([0, 1, 2], n_samples, p=[0.6, 0.25, 0.15])
    
    return pd.DataFrame({
        'head_tilt': np.clip(head_tilt, -30, 30),
        'shoulder_alignment': np.clip(shoulder_alignment, -20, 20),
        'spine_angle': np.clip(spine_angle, 60, 120),
        'label': label  # 0: Good, 1: Forward head, 2: Slouched
    })

def generate_patient_profile(patient_id, patient_type='normal', n_reports=10):
    """Generate a complete patient profile with historical data"""
    profile = {
        'patient_id': patient_id,
        'name': f'Patient {patient_id}',
        'age': np.random.randint(30, 70),
        'gender': np.random.choice(['M', 'F']),
        'reports': []
    }
    
    start_date = datetime.now() - timedelta(days=n_reports*7)
    
    # For improving type, generate all data at once for proper distribution
    if patient_type == 'improving':
        total_samples = n_reports * 2
        heartbeat_data = generate_heartbeat_data(total_samples, patient_type)
        glucose_data = generate_glucose_data(total_samples, patient_type)
        breathing_data = generate_breathing_data(total_samples, patient_type)
        speech_data = generate_speech_data(total_samples, patient_type)
        emotion_data = generate_emotion_data(total_samples, patient_type)
        posture_data = generate_posture_data(total_samples, patient_type)
    
    for i in range(n_reports):
        report_date = start_date + timedelta(days=i*7)
        
        # Generate single readings for this report
        if patient_type == 'improving':
            # Use data from the pre-generated improving datasets
            heartbeat = heartbeat_data.iloc[i].to_dict()
            glucose = glucose_data.iloc[i].to_dict()
            breathing = breathing_data.iloc[i].to_dict()
            speech = speech_data.iloc[i].to_dict()
            emotion = emotion_data.iloc[i].to_dict()
            posture = posture_data.iloc[i].to_dict()
        else:
            heartbeat = generate_heartbeat_data(1, patient_type).iloc[0].to_dict()
            glucose = generate_glucose_data(1, patient_type).iloc[0].to_dict()
            breathing = generate_breathing_data(1, patient_type).iloc[0].to_dict()
            speech = generate_speech_data(1, patient_type).iloc[0].to_dict()
            emotion = generate_emotion_data(1, patient_type).iloc[0].to_dict()
            posture = generate_posture_data(1, patient_type).iloc[0].to_dict()
        
        report = {
            'report_id': f'{patient_id}_R{i+1:03d}',
            'date': report_date.strftime('%Y-%m-%d'),
            'heartbeat': heartbeat,
            'glucose': glucose,
            'breathing': breathing,
            'speech': speech,
            'emotion': emotion,
            'posture': posture
        }
        
        profile['reports'].append(report)
    
    return profile

def main():
    """Generate all datasets"""
    os.makedirs('data/training', exist_ok=True)
    os.makedirs('data/patients', exist_ok=True)
    
    print("Generating training datasets...")
    
    # Training data for all models
    heartbeat_train = generate_heartbeat_data(2000, 'normal')
    heartbeat_train.to_csv('data/training/heartbeat_train.csv', index=False)
    
    glucose_train = generate_glucose_data(2000, 'normal')
    glucose_train.to_csv('data/training/glucose_train.csv', index=False)
    
    breathing_train = generate_breathing_data(2000, 'normal')
    breathing_train.to_csv('data/training/breathing_train.csv', index=False)
    
    speech_train = generate_speech_data(2000, 'normal')
    speech_train.to_csv('data/training/speech_train.csv', index=False)
    
    emotion_train = generate_emotion_data(2000, 'normal')
    emotion_train.to_csv('data/training/emotion_train.csv', index=False)
    
    posture_train = generate_posture_data(2000, 'normal')
    posture_train.to_csv('data/training/posture_train.csv', index=False)
    
    print("Training datasets created!")
    
    print("\nGenerating patient profiles...")
    
    # Patient A - Single report scenario
    patient_a = generate_patient_profile('A', 'normal', n_reports=1)
    with open('data/patients/patient_A.json', 'w') as f:
        json.dump(patient_a, f, indent=2)
    
    # Patient B - Progress tracking scenario
    patient_b = generate_patient_profile('B', 'improving', n_reports=12)
    with open('data/patients/patient_B.json', 'w') as f:
        json.dump(patient_b, f, indent=2)
    
    print("Patient profiles created!")
    print("\n✅ All data generated successfully!")
    print(f"   - Training data: data/training/")
    print(f"   - Patient A: data/patients/patient_A.json (1 report)")
    print(f"   - Patient B: data/patients/patient_B.json (12 reports)")

if __name__ == '__main__':
    main()