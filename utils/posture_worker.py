import sys, json

def run(image_path):
    try:
        import cv2
        import numpy as np

        img = cv2.imread(image_path)
        if img is None:
            print(json.dumps(None)); return

        h, w = img.shape[:2]
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        bg_color = float(np.percentile(gray, 75))
        person_mask = (gray < bg_color * 0.80).astype(np.uint8) * 255
        ks = (max(5, w // 80), max(5, h // 60))
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, ks)
        person_mask = cv2.morphologyEx(person_mask, cv2.MORPH_CLOSE, kernel)
        person_mask = cv2.morphologyEx(person_mask, cv2.MORPH_OPEN, kernel)

        contours, _ = cv2.findContours(person_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        large = [c for c in contours if cv2.contourArea(c) > h * w * 0.01]

        head_tilt = 0.0
        shoulder_alignment = 0.0
        spine_angle = 92.0

        if large:
            largest = max(large, key=cv2.contourArea)
            px, py, pw, ph = cv2.boundingRect(largest)

            def cx(t, b):
                r = person_mask[py+int(ph*t):py+int(ph*b), px:px+pw]
                cols = np.where(np.any(r > 0, axis=0))[0]
                return float(np.mean(cols)) + px if len(cols) > 0 else px + pw / 2.0

            head_x     = cx(0.00, 0.18)
            shoulder_x = cx(0.18, 0.38)
            hip_x      = cx(0.55, 0.75)

            lean_ratio  = (hip_x - head_x) / max(ph, 1)
            spine_angle = max(70.0, min(155.0, round(90.0 + lean_ratio * 130.0, 1)))
            head_tilt   = max(-45.0, min(45.0,
                            round((head_x - shoulder_x) / max(pw * 0.1, 1) * 15.0, 1)))

            fc = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = fc.detectMultiScale(gray, 1.1, 4, minSize=(30, 30))
            if len(faces) > 0:
                fx, fy, fw, fh = max(faces, key=lambda r: r[2] * r[3])
                shoulder_alignment = round((fx + fw / 2.0 - w / 2.0) / w * 20.0, 1)

        hp = max(0.0, abs(head_tilt) - 8.0) * 2.5
        sp = max(0.0, abs(shoulder_alignment) - 5.0) * 2.0
        xp = max(0.0, spine_angle - 95.0) * 2.0
        score = max(0.0, min(100.0, 100.0 - hp - sp - xp))

        print(json.dumps({
            'head_tilt':          head_tilt,
            'shoulder_alignment': round(shoulder_alignment, 1),
            'spine_angle':        spine_angle,
            'posture_score':      round(score, 1),
            'auto_detected':      True,
        }))
    except Exception as e:
        import traceback
        sys.stderr.write(f"Posture worker error: {e}\n{traceback.format_exc()}\n")
        print(json.dumps(None))

if __name__ == '__main__':
    run(sys.argv[1] if len(sys.argv) > 1 else '')