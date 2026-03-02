"""
Inference Module
Loads trained models and performs predictions
"""

import joblib
import numpy as np
import pandas as pd
import os

class ModelInference:
    """Handles loading and inference for all six models"""
    
    def __init__(self, models_dir='models'):
        self.models_dir = models_dir
        self.models = {}
        self.load_models()
    
    def load_models(self):
        """Load all trained models"""
        model_files = {
            'heartbeat': 'heartbeat_model.pkl',
            'glucose': 'glucose_model.pkl',
            'breathing': 'breathing_model.pkl',
            'speech': 'speech_model.pkl',
            'emotion': 'emotion_model.pkl',
            'posture': 'posture_model.pkl'
        }
        
        for name, filename in model_files.items():
            path = os.path.join(self.models_dir, filename)
            if os.path.exists(path):
                self.models[name] = joblib.load(path)
            else:
                raise FileNotFoundError(f"Model file not found: {path}")
    
    def predict_heartbeat(self, heart_rate, rr_interval_variance):
        """Predict heartbeat abnormality"""
        X = np.array([[heart_rate, rr_interval_variance]])
        prediction = self.models['heartbeat'].predict(X)[0]
        
        labels = ['Normal', 'Bradycardia', 'Tachycardia', 'Irregular']
        status = labels[prediction]
        
        # Calculate confidence/score
        if hasattr(self.models['heartbeat'], 'predict_proba'):
            proba = self.models['heartbeat'].predict_proba(X)[0]
            confidence = float(proba[prediction])
        else:
            confidence = 0.85
        
        return {
            'status': status,
            'prediction': int(prediction),
            'confidence': confidence,
            'heart_rate': float(heart_rate),
            'rr_variance': float(rr_interval_variance)
        }
    
    def predict_glucose(self, age, bmi, meal_timing, activity_level):
        """Predict glucose range"""
        X = np.array([[age, bmi, meal_timing, activity_level]])
        prediction = self.models['glucose'].predict(X)[0]
        
        labels = ['Low', 'Normal', 'High']
        range_label = labels[prediction]
        
        if hasattr(self.models['glucose'], 'predict_proba'):
            proba = self.models['glucose'].predict_proba(X)[0]
            confidence = float(proba[prediction])
        else:
            confidence = 0.85
        
        return {
            'range': range_label,
            'prediction': int(prediction),
            'confidence': confidence,
            'age': int(age),
            'bmi': float(bmi),
            'meal_timing': int(meal_timing),
            'activity_level': int(activity_level)
        }
    
    def predict_breathing(self, breathing_rate, breath_depth, rest_vs_exercise):
        """Predict breathing irregularity"""
        X = np.array([[breathing_rate, breath_depth, rest_vs_exercise]])
        prediction = self.models['breathing'].predict(X)[0]
        
        labels = ['Normal', 'Shallow Breathing', 'Irregular', 'Apnea Risk']
        status = labels[prediction]
        
        confidence = 0.85
        
        return {
            'status': status,
            'prediction': int(prediction),
            'confidence': confidence,
            'breathing_rate': float(breathing_rate),
            'breath_depth': float(breath_depth)
        }
    
    def predict_speech(self, speech_rate, pause_frequency, pitch_variability):
        """Predict speech pattern"""
        X = np.array([[speech_rate, pause_frequency, pitch_variability]])
        prediction = self.models['speech'].predict(X)[0]
        
        labels = ['Normal Speech', 'Slurred/Slow', 'Stressed Speech']
        pattern = labels[prediction]
        
        confidence = 0.85
        
        return {
            'pattern': pattern,
            'prediction': int(prediction),
            'confidence': confidence,
            'speech_rate': float(speech_rate),
            'pause_frequency': float(pause_frequency)
        }
    
    def predict_emotion(self, text_sentiment, voice_emotion, facial_emotion):
        """Predict emotional state"""
        X = np.array([[text_sentiment, voice_emotion, facial_emotion]])
        prediction = self.models['emotion'].predict(X)[0]
        
        labels = ['Happy', 'Neutral', 'Stressed', 'Sad']
        state = labels[prediction]
        
        confidence = 0.85
        
        return {
            'state': state,
            'prediction': int(prediction),
            'confidence': confidence,
            'text_sentiment': float(text_sentiment),
            'voice_emotion': float(voice_emotion),
            'facial_emotion': float(facial_emotion)
        }
    
    def predict_posture(self, head_tilt, shoulder_alignment, spine_angle):
        """Predict posture quality"""
        X = np.array([[head_tilt, shoulder_alignment, spine_angle]])
        prediction = self.models['posture'].predict(X)[0]
        
        labels = ['Good Posture', 'Forward Head Posture', 'Slouched Sitting']
        posture_type = labels[prediction]
        
        # Calculate posture score (0-100)
        score = self._calculate_posture_score(head_tilt, shoulder_alignment, spine_angle)
        
        confidence = 0.85
        
        return {
            'posture': posture_type,
            'prediction': int(prediction),
            'score': float(score),
            'confidence': confidence,
            'head_tilt': float(head_tilt),
            'shoulder_alignment': float(shoulder_alignment),
            'spine_angle': float(spine_angle)
        }
    
    def _calculate_posture_score(self, head_tilt, shoulder_alignment, spine_angle):
        """Calculate posture score from 0-100"""
        # Ideal values
        ideal_head_tilt = 0
        ideal_shoulder = 0
        ideal_spine = 90
        
        # Calculate deviations
        head_dev = abs(head_tilt - ideal_head_tilt) / 30
        shoulder_dev = abs(shoulder_alignment - ideal_shoulder) / 20
        spine_dev = abs(spine_angle - ideal_spine) / 30
        
        # Average deviation
        avg_dev = (head_dev + shoulder_dev + spine_dev) / 3
        
        # Convert to score (100 = perfect)
        score = max(0, 100 - (avg_dev * 100))
        
        return score
    
    def predict_all(self, patient_data):
        """Run all predictions on patient data"""
        results = {}
        
        # Heartbeat
        if 'heartbeat' in patient_data:
            hb = patient_data['heartbeat']
            results['heartbeat'] = self.predict_heartbeat(
                hb['heart_rate'],
                hb['rr_interval_variance']
            )
        
        # Glucose
        if 'glucose' in patient_data:
            gl = patient_data['glucose']
            results['glucose'] = self.predict_glucose(
                gl['age'],
                gl['bmi'],
                gl['meal_timing'],
                gl['activity_level']
            )
        
        # Breathing
        if 'breathing' in patient_data:
            br = patient_data['breathing']
            results['breathing'] = self.predict_breathing(
                br['breathing_rate'],
                br['breath_depth'],
                br['rest_vs_exercise']
            )
        
        # Speech
        if 'speech' in patient_data:
            sp = patient_data['speech']
            results['speech'] = self.predict_speech(
                sp['speech_rate'],
                sp['pause_frequency'],
                sp['pitch_variability']
            )
        
        # Emotion
        if 'emotion' in patient_data:
            em = patient_data['emotion']
            results['emotion'] = self.predict_emotion(
                em['text_sentiment'],
                em['voice_emotion'],
                em['facial_emotion']
            )
        
        # Posture
        if 'posture' in patient_data:
            ps = patient_data['posture']
            results['posture'] = self.predict_posture(
                ps['head_tilt'],
                ps['shoulder_alignment'],
                ps['spine_angle']
            )
        
        return results

# Singleton instance
_inference_engine = None

def get_inference_engine(models_dir='models'):
    """Get or create inference engine singleton"""
    global _inference_engine
    if _inference_engine is None:
        _inference_engine = ModelInference(models_dir)
    return _inference_engine