import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.pipeline import Pipeline
import joblib
import os

# ---------------------------------------------------------------------------
# Feature sets
# ---------------------------------------------------------------------------
RICH_FEATURES = [
    'speech_rate_wpm',
    'pause_count',
    'total_pause_duration_s',
    'mean_pitch_hz',
    'pitch_std_dev',
    'jitter_percent',
    'shimmer',
    'harmonics_to_noise_ratio_db',
    'articulation_score',
    'flesch_reading_ease',
    'grade_level',
    'filler_word_count',
]

LEGACY_FEATURES = ['speech_rate', 'pause_frequency', 'pitch_variability']


def train_speech_model():
    """Train speech pattern analysis model with notebook-derived features."""
    print("=" * 60)
    print("Training Model 4: Speech Pattern Analysis (Extended)")
    print("=" * 60)

    df = pd.read_csv('data/training/speech_train.csv')

    # Choose feature set based on what columns are available
    if all(f in df.columns for f in RICH_FEATURES):
        feature_cols = RICH_FEATURES
        print("✅ Using rich feature set (notebook-derived)")
    elif all(f in df.columns for f in LEGACY_FEATURES):
        feature_cols = LEGACY_FEATURES
        print("⚠️  Rich features not found – falling back to legacy 3-feature set.")
        print("   Re-run utils/generate_data.py to regenerate speech_train.csv.")
    else:
        raise ValueError(
            "speech_train.csv must contain either the rich feature columns "
            f"{RICH_FEATURES} or the legacy columns {LEGACY_FEATURES}."
        )

    X = df[feature_cols].fillna(df[feature_cols].median())
    y = df['label']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # GradientBoosting handles non-linear acoustic relationships better
    model = Pipeline([
        ('scaler', StandardScaler()),
        ('clf', GradientBoostingClassifier(
            n_estimators=200,
            max_depth=4,
            learning_rate=0.05,
            subsample=0.8,
            random_state=42
        ))
    ])

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print(f"\nModel Accuracy: {accuracy:.4f}")
    print("\nClassification Report:")
    print(classification_report(
        y_test, y_pred,
        target_names=['Normal', 'Slurred/Slow', 'Stressed']
    ))

    # Store the feature list inside the pipeline so inference can read it
    model.feature_names = feature_cols

    os.makedirs('models', exist_ok=True)
    joblib.dump(model, 'models/speech_model.pkl')
    print("\n✅ Model saved to models/speech_model.pkl")

    return model


if __name__ == '__main__':
    train_speech_model()
