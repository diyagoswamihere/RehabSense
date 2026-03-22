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
        heart_rate = np.concatenate([
            np.random.normal(95, 10, n_samples // 2),
            np.random.normal(78, 8,  n_samples // 2)
        ])
        rr_interval_variance = np.concatenate([
            np.random.normal(0.08, 0.02, n_samples // 2),
            np.random.normal(0.05, 0.01, n_samples // 2)
        ])
        label = np.concatenate([
            np.random.choice([1, 2, 3], n_samples // 2, p=[0.4, 0.4, 0.2]),
            np.random.choice([0, 1],    n_samples // 2, p=[0.7, 0.3])
        ])

    return pd.DataFrame({
        'heart_rate':           np.clip(heart_rate, 40, 180),
        'rr_interval_variance': np.clip(rr_interval_variance, 0.01, 0.15),
        'label': label   # 0: Normal, 1: Bradycardia, 2: Tachycardia, 3: Irregular
    })


def generate_glucose_data(n_samples=1000, patient_type='normal'):
    """Generate blood glucose estimation data"""
    age           = np.random.randint(25, 75, n_samples)
    bmi           = np.random.normal(25, 4, n_samples)
    meal_timing   = np.random.choice([0, 1, 2, 3], n_samples)
    activity_level = np.random.choice([0, 1, 2], n_samples)

    if patient_type == 'improving':
        glucose_range = np.concatenate([
            np.random.choice([0, 1, 2], n_samples // 2, p=[0.2, 0.3, 0.5]),
            np.random.choice([0, 1, 2], n_samples // 2, p=[0.1, 0.7, 0.2])
        ])
    else:
        glucose_range = np.random.choice([0, 1, 2], n_samples, p=[0.15, 0.7, 0.15])

    return pd.DataFrame({
        'age':            age,
        'bmi':            np.clip(bmi, 18, 40),
        'meal_timing':    meal_timing,
        'activity_level': activity_level,
        'glucose_range':  glucose_range   # 0: Low, 1: Normal, 2: High
    })


def generate_breathing_data(n_samples=1000, patient_type='normal'):
    """Generate breathing pattern data"""
    breathing_rate   = np.random.normal(16, 3, n_samples)
    breath_depth     = np.random.normal(0.5, 0.1, n_samples)
    rest_vs_exercise = np.random.choice([0, 1], n_samples, p=[0.7, 0.3])

    if patient_type == 'improving':
        label = np.concatenate([
            np.random.choice([0, 1, 2, 3], n_samples // 2, p=[0.4, 0.3, 0.2, 0.1]),
            np.random.choice([0, 1],        n_samples // 2, p=[0.8, 0.2])
        ])
    else:
        label = np.random.choice([0, 1, 2, 3], n_samples, p=[0.7, 0.15, 0.1, 0.05])

    return pd.DataFrame({
        'breathing_rate':   np.clip(breathing_rate, 8, 30),
        'breath_depth':     np.clip(breath_depth, 0.2, 1.0),
        'rest_vs_exercise': rest_vs_exercise,
        'label': label   # 0: Normal, 1: Shallow, 2: Irregular, 3: Apnea risk
    })


def generate_speech_data(n_samples=1000, patient_type='normal'):
    """
    Generate speech pattern data using the 12 notebook-derived features.

    Label semantics:
        0 – Normal Speech
        1 – Slurred / Slow
        2 – Stressed Speech

    Feature distributions are grounded in published clinical ranges:
        - Normal WPM:   120–180
        - Slurred WPM:  60–110  (slow, more pauses, poor clarity)
        - Stressed WPM: 160–220 (fast, elevated pitch, more filler words)
    """
    n = n_samples

    # ------------------------------------------------------------------ labels
    if patient_type == 'improving':
        label = np.concatenate([
            np.random.choice([0, 1, 2], n // 2, p=[0.3, 0.5, 0.2]),
            np.random.choice([0, 1],    n // 2, p=[0.8, 0.2])
        ])
    else:
        label = np.random.choice([0, 1, 2], n, p=[0.70, 0.15, 0.15])

    # ------------------------------------------------------------------ features
    # Speech rate (WPM)
    wpm = np.where(label == 0, np.random.normal(148, 18, n),
          np.where(label == 1, np.random.normal(85,  15, n),
                               np.random.normal(190, 20, n)))

    # Pause count (number of detected pauses in ~10 s clip)
    pause_count = np.where(label == 0, np.random.poisson(2.5, n),
                  np.where(label == 1, np.random.poisson(6.0, n),
                                       np.random.poisson(1.5, n)))

    # Total pause duration (seconds)
    total_pause_s = np.where(label == 0, np.random.exponential(0.8, n),
                    np.where(label == 1, np.random.exponential(2.5, n),
                                         np.random.exponential(0.4, n)))

    # Mean fundamental frequency (Hz) – typical male ~120 Hz, female ~220 Hz
    mean_pitch = np.where(label == 0, np.random.normal(175, 30, n),
                 np.where(label == 1, np.random.normal(155, 25, n),   # slightly lower
                                       np.random.normal(200, 35, n)))  # elevated under stress

    # Pitch standard deviation (Hz)
    pitch_std = np.where(label == 0, np.random.normal(25, 6, n),
                np.where(label == 1, np.random.normal(15, 5, n),   # monotone
                                      np.random.normal(40, 8, n))) # erratic

    # Jitter % – <1 % is normal; >1 % indicates instability
    jitter = np.where(label == 0, np.random.exponential(0.5, n) + 0.2,
             np.where(label == 1, np.random.exponential(1.2, n) + 0.5,
                                   np.random.exponential(0.7, n) + 0.3))

    # Shimmer (amplitude instability) – <0.06 normal
    shimmer = np.where(label == 0, np.random.exponential(0.025, n) + 0.01,
              np.where(label == 1, np.random.exponential(0.06,  n) + 0.03,
                                    np.random.exponential(0.03,  n) + 0.02))

    # HNR (dB) – >20 dB clear; <15 dB breathy/hoarse
    hnr = np.where(label == 0, np.random.normal(22, 3, n),
          np.where(label == 1, np.random.normal(14, 4, n),
                                np.random.normal(19, 4, n)))

    # ASR articulation/confidence score (0–1)
    articulation = np.where(label == 0, np.random.beta(9, 1.5, n),   # high ~0.85–0.99
                   np.where(label == 1, np.random.beta(4, 4,   n),   # mid  ~0.40–0.70
                                         np.random.beta(7, 2,   n))) # decent ~0.70–0.90

    # Flesch Reading Ease (0–100; higher = simpler)
    flesch = np.where(label == 0, np.random.normal(65, 10, n),
             np.where(label == 1, np.random.normal(75, 12, n),   # simpler words under duress
                                   np.random.normal(55, 12, n)))  # more complex under stress

    # Flesch-Kincaid Grade Level
    grade = np.where(label == 0, np.random.normal(8.0,  1.5, n),
            np.where(label == 1, np.random.normal(6.0,  1.5, n),
                                  np.random.normal(10.0, 2.0, n)))

    # Filler word count
    fillers = np.where(label == 0, np.random.poisson(1.0, n),
              np.where(label == 1, np.random.poisson(3.0, n),
                                    np.random.poisson(2.0, n)))

    return pd.DataFrame({
        'speech_rate_wpm':             np.clip(wpm,          50,  250),
        'pause_count':                 np.clip(pause_count,   0,   20).astype(int),
        'total_pause_duration_s':      np.clip(total_pause_s, 0,   15),
        'mean_pitch_hz':               np.clip(mean_pitch,   80,  350),
        'pitch_std_dev':               np.clip(pitch_std,     5,   80),
        'jitter_percent':              np.clip(jitter,        0,    5),
        'shimmer':                     np.clip(shimmer,       0,    0.3),
        'harmonics_to_noise_ratio_db': np.clip(hnr,           0,   35),
        'articulation_score':          np.clip(articulation,  0,    1),
        'flesch_reading_ease':         np.clip(flesch,        0,  100),
        'grade_level':                 np.clip(grade,         0,   18),
        'filler_word_count':           np.clip(fillers,       0,   15).astype(int),
        'label': label   # 0: Normal, 1: Slurred/Slow, 2: Stressed
    })


def generate_emotion_data(n_samples=1000, patient_type='normal'):
    """Generate emotional state data"""
    text_sentiment = np.random.normal(0.5, 0.2, n_samples)
    voice_emotion  = np.random.normal(0.5, 0.2, n_samples)
    facial_emotion = np.random.normal(0.5, 0.2, n_samples)

    if patient_type == 'improving':
        label = np.concatenate([
            np.random.choice([0, 1, 2, 3], n_samples // 2, p=[0.2, 0.2, 0.4, 0.2]),
            np.random.choice([0, 1, 2],    n_samples // 2, p=[0.5, 0.4, 0.1])
        ])
    else:
        label = np.random.choice([0, 1, 2, 3], n_samples, p=[0.4, 0.35, 0.15, 0.1])

    return pd.DataFrame({
        'text_sentiment': np.clip(text_sentiment, 0, 1),
        'voice_emotion':  np.clip(voice_emotion,  0, 1),
        'facial_emotion': np.clip(facial_emotion, 0, 1),
        'label': label   # 0: Happy, 1: Neutral, 2: Stressed, 3: Sad
    })


def generate_posture_data(n_samples=1000, patient_type='normal'):
    """Generate posture detection data"""
    head_tilt           = np.random.normal(0,  10, n_samples)
    shoulder_alignment  = np.random.normal(0,   8, n_samples)
    spine_angle         = np.random.normal(90, 15, n_samples)

    if patient_type == 'improving':
        label = np.concatenate([
            np.random.choice([0, 1, 2], n_samples // 2, p=[0.3, 0.4, 0.3]),
            np.random.choice([0, 1],    n_samples // 2, p=[0.7, 0.3])
        ])
    else:
        label = np.random.choice([0, 1, 2], n_samples, p=[0.6, 0.25, 0.15])

    return pd.DataFrame({
        'head_tilt':           np.clip(head_tilt,          -30, 30),
        'shoulder_alignment':  np.clip(shoulder_alignment, -20, 20),
        'spine_angle':         np.clip(spine_angle,         60, 120),
        'label': label   # 0: Good, 1: Forward head, 2: Slouched
    })


def _speech_row_to_dict(row: pd.Series) -> dict:
    """Convert a speech DataFrame row to the patient-report dict format."""
    return {
        'speech_rate_wpm':             float(row['speech_rate_wpm']),
        'pause_count':                 int(row['pause_count']),
        'total_pause_duration_s':      float(row['total_pause_duration_s']),
        'mean_pitch_hz':               float(row['mean_pitch_hz']),
        'pitch_std_dev':               float(row['pitch_std_dev']),
        'jitter_percent':              float(row['jitter_percent']),
        'shimmer':                     float(row['shimmer']),
        'harmonics_to_noise_ratio_db': float(row['harmonics_to_noise_ratio_db']),
        'articulation_score':          float(row['articulation_score']),
        'flesch_reading_ease':         float(row['flesch_reading_ease']),
        'grade_level':                 float(row['grade_level']),
        'filler_word_count':           int(row['filler_word_count']),
        'label':                       int(row['label']),
    }


def generate_patient_profile(patient_id, patient_type='normal', n_reports=10):
    """Generate a complete patient profile with historical data."""
    profile = {
        'patient_id': patient_id,
        'name':       f'Patient {patient_id}',
        'age':        int(np.random.randint(30, 70)),
        'gender':     str(np.random.choice(['M', 'F'])),
        'reports':    [],
    }

    start_date = datetime.now() - timedelta(days=n_reports * 7)

    if patient_type == 'improving':
        total_samples  = n_reports * 2
        heartbeat_data = generate_heartbeat_data(total_samples, patient_type)
        glucose_data   = generate_glucose_data(total_samples, patient_type)
        breathing_data = generate_breathing_data(total_samples, patient_type)
        speech_data    = generate_speech_data(total_samples, patient_type)
        emotion_data   = generate_emotion_data(total_samples, patient_type)
        posture_data   = generate_posture_data(total_samples, patient_type)

    for i in range(n_reports):
        report_date = start_date + timedelta(days=i * 7)

        if patient_type == 'improving':
            heartbeat = heartbeat_data.iloc[i].to_dict()
            glucose   = glucose_data.iloc[i].to_dict()
            breathing = breathing_data.iloc[i].to_dict()
            speech    = _speech_row_to_dict(speech_data.iloc[i])
            emotion   = emotion_data.iloc[i].to_dict()
            posture   = posture_data.iloc[i].to_dict()
        else:
            heartbeat = generate_heartbeat_data(1, patient_type).iloc[0].to_dict()
            glucose   = generate_glucose_data(1, patient_type).iloc[0].to_dict()
            breathing = generate_breathing_data(1, patient_type).iloc[0].to_dict()
            speech    = _speech_row_to_dict(generate_speech_data(1, patient_type).iloc[0])
            emotion   = generate_emotion_data(1, patient_type).iloc[0].to_dict()
            posture   = generate_posture_data(1, patient_type).iloc[0].to_dict()

        report = {
            'report_id': f'{patient_id}_R{i + 1:03d}',
            'date':      report_date.strftime('%Y-%m-%d'),
            'heartbeat': heartbeat,
            'glucose':   glucose,
            'breathing': breathing,
            'speech':    speech,
            'emotion':   emotion,
            'posture':   posture,
        }
        profile['reports'].append(report)

    return profile


def main():
    """Generate all datasets."""
    os.makedirs('data/training', exist_ok=True)
    os.makedirs('data/patients', exist_ok=True)

    print("Generating training datasets...")

    generate_heartbeat_data(2000, 'normal').to_csv('data/training/heartbeat_train.csv', index=False)
    generate_glucose_data(2000, 'normal').to_csv('data/training/glucose_train.csv', index=False)
    generate_breathing_data(2000, 'normal').to_csv('data/training/breathing_train.csv', index=False)
    generate_speech_data(2000, 'normal').to_csv('data/training/speech_train.csv', index=False)
    generate_emotion_data(2000, 'normal').to_csv('data/training/emotion_train.csv', index=False)
    generate_posture_data(2000, 'normal').to_csv('data/training/posture_train.csv', index=False)

    print("Training datasets created!")

    print("\nGenerating patient profiles...")

    patient_a = generate_patient_profile('A', 'normal', n_reports=1)
    with open('data/patients/patient_A.json', 'w') as f:
        json.dump(patient_a, f, indent=2)

    patient_b = generate_patient_profile('B', 'improving', n_reports=12)
    with open('data/patients/patient_B.json', 'w') as f:
        json.dump(patient_b, f, indent=2)

    print("Patient profiles created!")
    print("\n✅ All data generated successfully!")
    print("   - Training data : data/training/")
    print("   - Patient A     : data/patients/patient_A.json (1 report)")
    print("   - Patient B     : data/patients/patient_B.json (12 reports)")


if __name__ == '__main__':
    main()
