"""
Inference Module
Loads trained models and performs predictions.

The speech model now uses the full notebook-derived analysis pipeline:
    • Transcription + articulation score  (SpeechRecognition / Google API)
    • Voice quality metrics               (parselmouth / Praat)
    • Fluency & speech rate               (librosa)
    • Language & cognitive load           (textstat)
"""

import joblib
import numpy as np
import pandas as pd
import os

# ---------------------------------------------------------------------------
# Optional heavy imports for speech analysis
# Imported lazily so the rest of the app still loads if they are absent.
# ---------------------------------------------------------------------------
try:
    import librosa
    _LIBROSA_OK = True
except ImportError:
    _LIBROSA_OK = False

try:
    import parselmouth
    from parselmouth.praat import call as praat_call
    _PARSELMOUTH_OK = True
except ImportError:
    _PARSELMOUTH_OK = False

try:
    import speech_recognition as sr
    _SR_OK = True
except ImportError:
    _SR_OK = False

try:
    import textstat
    _TEXTSTAT_OK = True
except ImportError:
    _TEXTSTAT_OK = False

try:
    import ffmpeg
    _FFMPEG_OK = True
except ImportError:
    _FFMPEG_OK = False


# ---------------------------------------------------------------------------
# Standalone speech-analysis helpers (ported from notebook)
# ---------------------------------------------------------------------------

def _preprocess_audio(audio_file_path: str) -> str:
    """
    Normalise audio to 16-kHz mono PCM WAV using ffmpeg.
    Returns path to the processed file.
    """
    if not _FFMPEG_OK:
        return audio_file_path
    processed = "processed_speech_tmp.wav"
    try:
        (
            ffmpeg
            .input(audio_file_path)
            .output(processed, acodec='pcm_s16le', ar='16000', ac='1')
            .run(overwrite_output=True, capture_stdout=True, capture_stderr=True)
        )
        return processed
    except Exception:
        return audio_file_path


def transcribe_audio(audio_file_path: str):
    """
    Transcribe speech and return (transcript, articulation_score).
    articulation_score is the Google ASR confidence (0–1).
    """
    if not _SR_OK:
        return "Speech recognition not available.", 0.0

    processed = _preprocess_audio(audio_file_path)
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(processed) as source:
            audio_data = recognizer.record(source)

        response = recognizer.recognize_google(audio_data, show_all=True)
        if processed != audio_file_path and os.path.exists(processed):
            os.remove(processed)

        if not response or not response.get("alternative"):
            return "Could not understand audio.", 0.0

        best = response["alternative"][0]
        transcript = best.get("transcript", "")
        confidence = best.get("confidence", 0.0)
        return transcript, round(float(confidence), 3)

    except sr.UnknownValueError:
        return "Could not understand the audio.", 0.0
    except sr.RequestError as e:
        return f"API request failed; {e}", 0.0
    except Exception as e:
        return f"Transcription error: {e}", 0.0


def analyze_voice_quality(audio_file_path: str) -> dict:
    """
    Extract acoustic voice-quality metrics using Praat (parselmouth).
    Returns: mean_pitch_hz, pitch_std_dev, jitter_percent, shimmer,
             harmonics_to_noise_ratio_db
    """
    nan = float('nan')
    defaults = {
        "mean_pitch_hz": nan,
        "pitch_std_dev": nan,
        "jitter_percent": nan,
        "shimmer": nan,
        "harmonics_to_noise_ratio_db": nan,
    }
    if not _PARSELMOUTH_OK:
        return defaults

    try:
        sound = parselmouth.Sound(audio_file_path)

        # Pitch
        try:
            pitch_obj = praat_call(sound, "To Pitch", 0.0, 75, 600)
            mean_pitch = praat_call(pitch_obj, "Get mean", 0, 0, "Hertz")
            std_pitch  = praat_call(pitch_obj, "Get standard deviation", 0, 0, "Hertz")
        except parselmouth.PraatError:
            mean_pitch = std_pitch = nan

        # Jitter
        try:
            pp = praat_call(sound, "To PointProcess (periodic, cc)", 75, 600)
            jitter = praat_call(pp, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3) * 100
        except parselmouth.PraatError:
            jitter = nan

        # Shimmer
        try:
            pp2 = praat_call(sound, "To PointProcess (periodic, cc)", 75, 600)
            shimmer = praat_call(pp2, "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
        except parselmouth.PraatError:
            shimmer = nan

        # HNR
        try:
            harmonicity = praat_call(sound, "To Harmonicity (cc)", 0.01, 75, 0.1, 1.0)
            hnr = praat_call(harmonicity, "Get mean", 0, 0)
        except parselmouth.PraatError:
            hnr = nan

        def _r(v):
            return round(float(v), 4) if not (v != v) else nan  # NaN-safe round

        return {
            "mean_pitch_hz": _r(mean_pitch),
            "pitch_std_dev": _r(std_pitch),
            "jitter_percent": _r(jitter),
            "shimmer": _r(shimmer),
            "harmonics_to_noise_ratio_db": _r(hnr),
        }
    except Exception:
        return defaults


def assess_fluency_and_rate(audio_file_path: str, transcript: str) -> dict:
    """
    Compute speech rate (WPM), pause count, and total pause duration.
    """
    if not _LIBROSA_OK:
        return {
            "speech_rate_wpm": 0.0,
            "word_count": len(transcript.split()),
            "audio_duration_s": 0.0,
            "pause_count": 0,
            "total_pause_duration_s": 0.0,
        }

    y_audio, sr_rate = librosa.load(audio_file_path, sr=None)
    duration_s = librosa.get_duration(y=y_audio, sr=sr_rate)
    word_count = len(transcript.split())
    wpm = (word_count / duration_s) * 60 if duration_s > 0 else 0.0

    intervals = librosa.effects.split(y=y_audio, top_db=20)
    pause_count = max(len(intervals) - 1, 0)
    total_pause_s = 0.0
    if pause_count > 0:
        pause_durations = [
            intervals[i][0] - intervals[i - 1][1]
            for i in range(1, len(intervals))
        ]
        total_pause_s = float(np.sum(pause_durations)) / sr_rate

    return {
        "speech_rate_wpm": round(wpm, 2),
        "word_count": word_count,
        "audio_duration_s": round(duration_s, 2),
        "pause_count": pause_count,
        "total_pause_duration_s": round(total_pause_s, 2),
    }


def analyze_language_and_cognition(transcript: str) -> dict:
    """
    Measure language complexity and cognitive-load proxies.
    """
    defaults = {"flesch_reading_ease": 0.0, "grade_level": 0.0, "filler_word_count": 0}
    if not _TEXTSTAT_OK or not transcript or len(transcript.split()) < 5:
        return defaults

    filler_words = {"uh", "um", "hmm", "er", "like", "you know"}
    filler_count = sum(1 for w in transcript.lower().split() if w in filler_words)

    return {
        "flesch_reading_ease": textstat.flesch_reading_ease(transcript),
        "grade_level": textstat.flesch_kincaid_grade(transcript),
        "filler_word_count": filler_count,
    }


def analyze_speech_from_audio(audio_file_path: str) -> dict:
    """
    Full notebook pipeline on a WAV file.
    Returns all extracted features plus the ML-model prediction.
    This is the single entry-point called from Flask.
    """
    transcript, articulation_score = transcribe_audio(audio_file_path)
    voice_quality   = analyze_voice_quality(audio_file_path)
    fluency         = assess_fluency_and_rate(audio_file_path, transcript)
    lang_cog        = analyze_language_and_cognition(transcript)

    return {
        "transcript": transcript,
        "articulation_score": articulation_score,
        **voice_quality,
        **fluency,
        **lang_cog,
    }


# ---------------------------------------------------------------------------
# Inference engine
# ---------------------------------------------------------------------------

class ModelInference:
    """Handles loading and inference for all six models."""

    def __init__(self, models_dir='models'):
        self.models_dir = models_dir
        self.models = {}
        self.load_models()

    def load_models(self):
        """Load all trained models."""
        model_files = {
            'heartbeat': 'heartbeat_model.pkl',
            'glucose':   'glucose_model.pkl',
            'breathing': 'breathing_model.pkl',
            'speech':    'speech_model.pkl',
            'emotion':   'emotion_model.pkl',
            'posture':   'posture_model.pkl',
        }
        for name, filename in model_files.items():
            path = os.path.join(self.models_dir, filename)
            if os.path.exists(path):
                self.models[name] = joblib.load(path)
            else:
                raise FileNotFoundError(f"Model file not found: {path}")

    # ------------------------------------------------------------------
    # Individual predictors
    # ------------------------------------------------------------------

    def predict_heartbeat(self, heart_rate, rr_interval_variance):
        X = np.array([[heart_rate, rr_interval_variance]])
        prediction = self.models['heartbeat'].predict(X)[0]
        labels = ['status_normal', 'status_bradycardia', 'status_tachycardia', 'status_irregular']
        status = labels[prediction]
        confidence = 0.85
        if hasattr(self.models['heartbeat'], 'predict_proba'):
            proba = self.models['heartbeat'].predict_proba(X)[0]
            confidence = float(proba[prediction])
        return {
            'status': status, 'prediction': int(prediction),
            'confidence': confidence,
            'heart_rate': float(heart_rate),
            'rr_variance': float(rr_interval_variance),
        }

    def predict_glucose(self, age, bmi, meal_timing, activity_level):
        X = np.array([[age, bmi, meal_timing, activity_level]])
        prediction = self.models['glucose'].predict(X)[0]
        labels = ['status_low', 'status_normal', 'status_high']
        range_label = labels[prediction]
        confidence = 0.85
        if hasattr(self.models['glucose'], 'predict_proba'):
            proba = self.models['glucose'].predict_proba(X)[0]
            confidence = float(proba[prediction])
        return {
            'range': range_label, 'prediction': int(prediction),
            'confidence': confidence,
            'age': int(age), 'bmi': float(bmi),
            'meal_timing': int(meal_timing), 'activity_level': int(activity_level),
        }

    def predict_breathing(self, breathing_rate, breath_depth, rest_vs_exercise):
        X = np.array([[breathing_rate, breath_depth, rest_vs_exercise]])
        prediction = self.models['breathing'].predict(X)[0]
        labels = ['status_normal', 'status_shallow_breathing', 'status_irregular', 'status_apnea_risk']
        status = labels[prediction]
        return {
            'status': status, 'prediction': int(prediction),
            'confidence': 0.85,
            'breathing_rate': float(breathing_rate),
            'breath_depth': float(breath_depth),
        }

    def predict_speech(self, speech_rate=None, pause_frequency=None,
                       pitch_variability=None, audio_file_path=None,
                       **extra_features):
        """
        Predict speech pattern.

        Two calling modes:
        1. audio_file_path supplied → runs the full notebook pipeline to extract
           all features, then classifies.
        2. Numeric kwargs supplied (legacy / from stored patient JSON) → builds
           the feature vector directly from the provided values.
        """
        model = self.models['speech']
        feature_names = getattr(model, 'feature_names', None)

        # ---- Mode 1: real audio file ----
        if audio_file_path is not None:
            raw = analyze_speech_from_audio(audio_file_path)
            features = raw  # dict with all extracted values
        else:
            # ---- Mode 2: numeric inputs (legacy or patient JSON) ----
            features = {}
            if feature_names and feature_names != ['speech_rate', 'pause_frequency', 'pitch_variability']:
                # Rich-feature model – map legacy fields if needed
                features = {
                    'speech_rate_wpm':             float(speech_rate or 120),
                    'pause_count':                 float(pause_frequency or 0) * 10,
                    'total_pause_duration_s':      0.0,
                    'mean_pitch_hz':               200.0,
                    'pitch_std_dev':               float(pitch_variability or 20) * 50,
                    'jitter_percent':              1.0,
                    'shimmer':                     0.05,
                    'harmonics_to_noise_ratio_db': 15.0,
                    'articulation_score':          0.85,
                    'flesch_reading_ease':         60.0,
                    'grade_level':                 8.0,
                    'filler_word_count':           0,
                    **extra_features,
                }
            else:
                features = {
                    'speech_rate':      float(speech_rate or 120),
                    'pause_frequency':  float(pause_frequency or 0.1),
                    'pitch_variability': float(pitch_variability or 0.3),
                }

        # Build input array respecting the model's expected column order
        if feature_names:
            row = [features.get(f, 0.0) for f in feature_names]
        else:
            row = [features.get('speech_rate', 120),
                   features.get('pause_frequency', 0.1),
                   features.get('pitch_variability', 0.3)]

        X = np.array([row])
        prediction = model.predict(X)[0]

        labels = ['status_normal_speech', 'status_slurred_speech', 'status_stressed_speech']
        pattern = labels[int(prediction)]

        confidence = 0.85
        if hasattr(model, 'predict_proba'):
            proba = model.predict_proba(X)[0]
            confidence = float(proba[prediction])

        result = {
            'pattern':     pattern,
            'prediction':  int(prediction),
            'confidence':  confidence,
        }

        # Attach transcript + rich metrics when we ran the audio pipeline
        if audio_file_path is not None:
            result['transcript']        = features.get('transcript', '')
            result['articulation_score'] = features.get('articulation_score', 0.0)
            result['speech_rate_wpm']   = features.get('speech_rate_wpm', 0.0)
            result['pause_count']       = features.get('pause_count', 0)
            result['total_pause_duration_s'] = features.get('total_pause_duration_s', 0.0)
            result['mean_pitch_hz']     = features.get('mean_pitch_hz', 0.0)
            result['pitch_std_dev']     = features.get('pitch_std_dev', 0.0)
            result['jitter_percent']    = features.get('jitter_percent', 0.0)
            result['shimmer']           = features.get('shimmer', 0.0)
            result['harmonics_to_noise_ratio_db'] = features.get('harmonics_to_noise_ratio_db', 0.0)
            result['flesch_reading_ease'] = features.get('flesch_reading_ease', 0.0)
            result['grade_level']       = features.get('grade_level', 0.0)
            result['filler_word_count'] = features.get('filler_word_count', 0)
            result['interpretation']    = _interpretation_guide(result)
        else:
            result['speech_rate']       = float(speech_rate or 120)
            result['pause_frequency']   = float(pause_frequency or 0.1)

        return result

    def predict_emotion(self, text_sentiment, voice_emotion, facial_emotion):
        X = np.array([[text_sentiment, voice_emotion, facial_emotion]])
        prediction = self.models['emotion'].predict(X)[0]
        labels = ['status_happy', 'status_neutral', 'status_stressed', 'status_sad']
        state = labels[prediction]
        return {
            'state': state, 'prediction': int(prediction),
            'confidence': 0.85,
            'text_sentiment': float(text_sentiment),
            'voice_emotion': float(voice_emotion),
            'facial_emotion': float(facial_emotion),
        }

    def predict_posture(self, head_tilt, shoulder_alignment, spine_angle):
        X = np.array([[head_tilt, shoulder_alignment, spine_angle]])
        prediction = self.models['posture'].predict(X)[0]
        labels = ['status_good_posture', 'status_forward_head', 'status_slouched']
        posture_type = labels[prediction]
        score = self._calculate_posture_score(head_tilt, shoulder_alignment, spine_angle)
        return {
            'posture': posture_type, 'status': posture_type, 'prediction': int(prediction),
            'posture_score': float(score), 'score': float(score), 'confidence': 0.85,
            'head_tilt': float(head_tilt),
            'shoulder_alignment': float(shoulder_alignment),
            'spine_angle': float(spine_angle),
        }

    def _calculate_posture_score(self, head_tilt, shoulder_alignment, spine_angle):
        head_dev     = abs(head_tilt - 0) / 30
        shoulder_dev = abs(shoulder_alignment - 0) / 20
        spine_dev    = abs(spine_angle - 90) / 30
        avg_dev = (head_dev + shoulder_dev + spine_dev) / 3
        return max(0, 100 - avg_dev * 100)

    def predict_all(self, patient_data):
        """Run all predictions on patient data dict."""
        results = {}

        if 'heartbeat' in patient_data:
            hb = patient_data['heartbeat']
            results['heartbeat'] = self.predict_heartbeat(
                hb['heart_rate'], hb['rr_interval_variance'])

        if 'glucose' in patient_data:
            gl = patient_data['glucose']
            results['glucose'] = self.predict_glucose(
                gl['age'], gl['bmi'], gl['meal_timing'], gl['activity_level'])

        if 'breathing' in patient_data:
            br = patient_data['breathing']
            results['breathing'] = self.predict_breathing(
                br['breathing_rate'], br['breath_depth'], br['rest_vs_exercise'])

        if 'speech' in patient_data:
            sp = patient_data['speech']
            # Support audio path stored in patient JSON or raw numeric fields
            if 'audio_file_path' in sp:
                results['speech'] = self.predict_speech(
                    audio_file_path=sp['audio_file_path'])
            else:
                results['speech'] = self.predict_speech(
                    speech_rate=sp.get('speech_rate'),
                    pause_frequency=sp.get('pause_frequency'),
                    pitch_variability=sp.get('pitch_variability'))

        if 'emotion' in patient_data:
            em = patient_data['emotion']
            results['emotion'] = self.predict_emotion(
                em['text_sentiment'], em['voice_emotion'], em['facial_emotion'])

        if 'posture' in patient_data:
            ps = patient_data['posture']
            results['posture'] = self.predict_posture(
                ps['head_tilt'], ps['shoulder_alignment'], ps['spine_angle'])

        return results


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _interpretation_guide(result: dict) -> dict:
    """Return per-metric rehab interpretation flags."""
    return {
        "articulation": (
            "Clear articulation" if result.get('articulation_score', 0) > 0.8
            else "Unclear articulation – may need speech therapy focus"
        ),
        "speech_rate": (
            "Appropriate rate" if 80 <= result.get('speech_rate_wpm', 0) <= 180
            else "Rate outside typical range (80–180 WPM)"
        ),
        "jitter": (
            "Stable vocal fold vibration"
            if result.get('jitter_percent', 99) < 1.0
            else "Elevated jitter – possible vocal instability"
        ),
        "hnr": (
            "Clear voice quality"
            if result.get('harmonics_to_noise_ratio_db', 0) > 20
            else "Breathy/hoarse voice – monitor for improvement"
        ),
        "pauses": (
            "Fluent with minimal hesitations"
            if result.get('pause_count', 0) <= 3
            else "Frequent pauses – may indicate word-finding difficulty"
        ),
    }


# ---------------------------------------------------------------------------
# Singleton
# ---------------------------------------------------------------------------
_inference_engine = None


def get_inference_engine(models_dir='models'):
    global _inference_engine
    if _inference_engine is None:
        _inference_engine = ModelInference(models_dir)
    return _inference_engine


# ---------------------------------------------------------------------------
# Image-based posture analysis (OpenCV)
# ---------------------------------------------------------------------------


def analyze_posture_from_image(image_path: str) -> dict:
    """Run posture analysis in a subprocess — keeps cv2 DLLs out of Flask process.
    Prevents crashes on Windows Python 3.13 + Flask dev server."""
    try:
        import subprocess, json, sys, os
        worker = os.path.join(os.path.dirname(__file__), 'posture_worker.py')
        result = subprocess.run(
            [sys.executable, worker, image_path],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode != 0:
            print(f"Posture worker stderr: {result.stderr[:300]}")
            return None
        output = result.stdout.strip()
        if not output or output == 'null':
            return None
        data = json.loads(output)
        if data:
            print(f"Posture: tilt={data['head_tilt']} spine={data['spine_angle']} score={data['posture_score']:.0f}")
        return data
    except subprocess.TimeoutExpired:
        print("Posture worker timed out")
        return None
    except Exception as e:
        print(f"Posture analysis error: {e}")
        return None


def analyze_audio_complete(audio_path: str) -> dict:
    """Run audio analysis in a subprocess to avoid DLL/thread crashes on Windows.
    Calls utils/audio_worker.py via subprocess — isolates librosa from Flask process."""
    try:
        import subprocess, json, sys, os

        worker = os.path.join(os.path.dirname(__file__), 'audio_worker.py')
        result = subprocess.run(
            [sys.executable, worker, audio_path],
            capture_output=True, text=True, timeout=40
        )
        if result.returncode != 0:
            print(f"Audio worker stderr: {result.stderr[:300]}")
            return None
        output = result.stdout.strip()
        if not output or output == 'null':
            return None
        data = json.loads(output)
        if data:
            print(f"Audio: {data['duration_sec']}s {data['speech_rate']}wpm energy={data['voice_energy']:.2f}")
        return data
    except subprocess.TimeoutExpired:
        print("Audio worker timed out after 40s")
        return None
    except Exception as e:
        print(f"Audio analysis error: {e}")
        return None