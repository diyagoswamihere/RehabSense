import sys, json

def run(audio_path):
    try:
        import librosa
        import numpy as np

        y_full, sr = librosa.load(audio_path, sr=None, mono=True)
        y = y_full[:sr * 60] if len(y_full) > sr * 60 else y_full
        duration = len(y) / sr
        if duration < 0.5:
            print(json.dumps(None)); return

        intervals       = librosa.effects.split(y, top_db=30)
        speech_seconds  = sum((e - s) for s, e in intervals) / sr
        speech_rate_wpm = int(round(max(1, speech_seconds / 0.45) / max(duration / 60.0, 0.01)))
        pause_count     = max(0, len(intervals) - 1)
        pause_freq      = round(min(1.0, pause_count / max(1, duration / 10)), 3)

        rms          = librosa.feature.rms(y=y, frame_length=512, hop_length=256)[0]
        voice_energy = round(min(1.0, float(np.mean(rms)) * 12), 3)

        zcr       = librosa.feature.zero_crossing_rate(y, frame_length=512, hop_length=256)[0]
        pitch_var = round(min(1.0, float(np.std(zcr)) * 20), 3)

        centroid     = librosa.feature.spectral_centroid(y=y, sr=sr, hop_length=256)[0]
        bright_score = round(min(1.0, float(np.mean(centroid)) / 3000.0), 3)

        voice_emotion  = round(pitch_var * 0.4 + voice_energy * 0.4 + bright_score * 0.2, 3)
        rate_norm      = min(1.0, speech_rate_wpm / 160.0)
        text_sentiment = round(min(1.0, max(0.0,
            rate_norm * 0.4 + voice_energy * 0.35 + (1 - pause_freq) * 0.25)), 3)

        result = {
            'speech_rate':       speech_rate_wpm,
            'pause_frequency':   pause_freq,
            'pitch_variability': pitch_var,
            'voice_energy':      voice_energy,
            'voice_emotion':     voice_emotion,
            'text_sentiment':    text_sentiment,
            'duration_sec':      round(duration, 1),
            'auto_detected':     True,
        }
        print(json.dumps(result))
    except Exception as e:
        import traceback
        sys.stderr.write(f"Audio worker error: {e}\n{traceback.format_exc()}\n")
        print(json.dumps(None))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(json.dumps(None))
    else:
        run(sys.argv[1])