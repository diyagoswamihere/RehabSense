"""
RehabSense Backend Server
Flask application serving the rehabilitation monitoring portal
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import json
import os
import sys
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils.inference import get_inference_engine
from recommendations.engine import get_all_recommendations, get_summary_message

# Resolve absolute project paths for resources
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
TEMPLATES_DIR = os.path.join(PROJECT_ROOT, 'frontend', 'templates')
STATIC_DIR = os.path.join(PROJECT_ROOT, 'frontend', 'static')
MODELS_DIR = os.path.join(PROJECT_ROOT, 'models')
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')

app = Flask(__name__, 
            template_folder=TEMPLATES_DIR,
            static_folder=STATIC_DIR)
app.secret_key = 'rehabsense_secret_key_2026'

# Initialize inference engine with absolute models path
try:
    inference_engine = get_inference_engine(MODELS_DIR)
    print("✅ Inference engine loaded successfully")
except Exception as e:
    print(f"❌ Error loading models: {e}")
    print("Please run training/train_all.py first")
    sys.exit(1)


def _get_patient_filename(patient_id: str) -> str:
    """Resolve patient JSON filename from patient_id."""
    file_mapping = {
        '1D55PL6': 'patient_A.json',
        '7D42PL2': 'patient_B.json'
    }
    return file_mapping.get(patient_id, f'patient_{patient_id}.json')


def load_patient_data(patient_id):
    """Load patient data from JSON file."""
    filename = _get_patient_filename(patient_id)
    filepath = os.path.join(DATA_DIR, 'patients', filename)

    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    return None


def save_patient_data(patient):
    """Persist patient JSON to disk."""
    patient_id = patient.get('patient_id')
    if not patient_id:
        raise ValueError("patient_id is required to save patient data")

    filename = _get_patient_filename(patient_id)
    filepath = os.path.join(DATA_DIR, 'patients', filename)

    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        json.dump(patient, f, indent=2)


def load_all_patients():
    """Load all patients for admin dashboard."""
    patients_dir = os.path.join(DATA_DIR, 'patients')
    if not os.path.exists(patients_dir):
        return []

    patients = []
    for fname in os.listdir(patients_dir):
        if not fname.endswith('.json'):
            continue
        fpath = os.path.join(patients_dir, fname)
        with open(fpath, 'r') as f:
            try:
                patient = json.load(f)
                patients.append(patient)
            except json.JSONDecodeError:
                continue
    return patients

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    """Patient login with new credentials"""
    data = request.json
    patient_id = data.get('patient_id', '').upper()
    password = data.get('password', '')
    
    # Check new patient credentials
    if patient_id == '1D55PL6' and password == 'newp@117789':
        session['patient_id'] = '1D55PL6'
        patient_data = load_patient_data('1D55PL6')
        
        if patient_data:
            return jsonify({
                'success': True,
                'patient': patient_data
            })
    
    elif patient_id == '7D42PL2' and password == 'neww@342217':
        session['patient_id'] = '7D42PL2'
        patient_data = load_patient_data('7D42PL2')
        
        if patient_data:
            return jsonify({
                'success': True,
                'patient': patient_data
            })
    
    return jsonify({'success': False, 'message': 'Invalid patient ID or password.'})

@app.route('/logout')
def logout():
    """Logout"""
    session.pop('patient_id', None)
    session.pop('is_admin', None)
    # After logout, send the user back to the main portal page
    return redirect(url_for('index'))


@app.route('/admin/login', methods=['POST'])
def admin_login():
    """Simple admin login with fixed credentials."""
    data = request.json
    email = data.get('email', '')
    password = data.get('password', '')

    if email == 'capstoneg_4@gmail.com' and password == 'lastreview@3451':
        session['is_admin'] = True
        return jsonify({'success': True})

    return jsonify({'success': False, 'message': 'Invalid admin credentials.'})


@app.route('/admin/dashboard')
def admin_dashboard():
    """Admin dashboard showing all patients."""
    if not session.get('is_admin'):
        return redirect(url_for('index'))

    patients = load_all_patients()
    # Do not expose passwords in templates
    for p in patients:
        p.pop('password', None)

    return render_template('admin_dashboard.html', patients=patients)


@app.route('/admin/patients/add', methods=['POST'])
def admin_add_patient():
    """Add a new patient record (basic demographic details)."""
    if not session.get('is_admin'):
        return jsonify({'success': False, 'message': 'Not authorized'}), 403

    data = request.json or {}
    required_fields = ['patient_id', 'name', 'age']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'success': False, 'message': f'Missing field: {field}'}), 400

    patient_id = data['patient_id'].upper()
    existing = load_patient_data(patient_id)
    if existing:
        return jsonify({'success': False, 'message': 'Patient ID already exists'}), 400

    new_patient = {
        'patient_id': patient_id,
        'name': data['name'],
        'age': data.get('age'),
        'gender': data.get('gender'),
        'address': data.get('address'),
        'phone': data.get('phone'),
        'email': data.get('email'),
        'consulting_doctor': data.get('consulting_doctor'),
        'allergies': data.get('allergies'),
        'image': data.get('image'),  # optional URL or filename
        'password': data.get('password', ''),
        'reports': []
    }

    save_patient_data(new_patient)
    return jsonify({'success': True, 'patient': new_patient})


@app.route('/admin/patient/<patient_id>/reports/add-data', methods=['POST'])
def admin_add_report_data(patient_id):
    """Admin manually enters structured report data."""
    if not session.get('is_admin'):
        return jsonify({'success': False, 'message': 'Not authorized'}), 403

    patient = load_patient_data(patient_id)
    if not patient:
        return jsonify({'success': False, 'message': 'Patient not found'}), 404

    data = request.json or {}

    reports = patient.get('reports', [])
    next_index = len(reports) + 1
    report_id = f"{patient_id}_R{next_index:03d}"

    new_report = {
        'report_id': report_id,
        'date': datetime.today().strftime('%Y-%m-%d'),
        'heartbeat': {
            'heart_rate': float(data.get('heart_rate', 0)),
            'rr_interval_variance': float(data.get('rr_interval_variance', 0)),
            'label': float(data.get('heartbeat_label', 0)),
        },
        'glucose': {
            'age': float(data.get('glucose_age', 0)),
            'bmi': float(data.get('bmi', 0)),
            'meal_timing': float(data.get('meal_timing', 0)),
            'activity_level': float(data.get('activity_level', 0)),
            'glucose_range': float(data.get('glucose_range', 0)),
        },
        'breathing': {
            'breathing_rate': float(data.get('breathing_rate', 0)),
            'breath_depth': float(data.get('breath_depth', 0)),
            'rest_vs_exercise': float(data.get('rest_vs_exercise', 0)),
            'label': float(data.get('breathing_label', 0)),
        },
        'speech': {
            'speech_rate': float(data.get('speech_rate', 0)),
            'pause_frequency': float(data.get('pause_frequency', 0)),
            'pitch_variability': float(data.get('pitch_variability', 0)),
            'label': float(data.get('speech_label', 0)),
        },
        'emotion': {
            'text_sentiment': float(data.get('text_sentiment', 0)),
            'voice_emotion': float(data.get('voice_emotion', 0)),
            'facial_emotion': float(data.get('facial_emotion', 0)),
            'label': float(data.get('emotion_label', 0)),
        },
        'posture': {
            'head_tilt': float(data.get('head_tilt', 0)),
            'shoulder_alignment': float(data.get('shoulder_alignment', 0)),
            'spine_angle': float(data.get('spine_angle', 0)),
            'label': float(data.get('posture_label', 0)),
        },
    }

    reports.append(new_report)
    patient['reports'] = reports
    save_patient_data(patient)

    return jsonify({'success': True, 'report': new_report})


@app.route('/admin/patient/<patient_id>/reports/upload', methods=['POST'])
def admin_upload_report(patient_id):
    """Admin uploads a report file (CSV, DOCX, etc.)."""
    if not session.get('is_admin'):
        return jsonify({'success': False, 'message': 'Not authorized'}), 403

    patient = load_patient_data(patient_id)
    if not patient:
        return jsonify({'success': False, 'message': 'Patient not found'}), 404

    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'Empty filename'}), 400

    uploads_dir = os.path.join(DATA_DIR, 'uploads', patient_id)
    os.makedirs(uploads_dir, exist_ok=True)
    filepath = os.path.join(uploads_dir, file.filename)
    file.save(filepath)

    reports = patient.get('reports', [])
    next_index = len(reports) + 1
    report_id = f"{patient_id}_U{next_index:03d}"

    new_report = {
        'report_id': report_id,
        'date': datetime.today().strftime('%Y-%m-%d'),
        'uploaded_file': filepath,
    }

    reports.append(new_report)
    patient['reports'] = reports
    save_patient_data(patient)

    return jsonify({'success': True, 'report': new_report})

@app.route('/dashboard')
def dashboard():
    """Patient dashboard with new design"""
    if 'patient_id' not in session:
        return render_template('index.html')
    
    patient_id = session['patient_id']
    patient_data = load_patient_data(patient_id)
    
    if not patient_data:
        return "Patient data not found", 404
    
    # Use the existing dashboard template
    return render_template('dashboard.html', patient=patient_data)

@app.route('/api/predict', methods=['POST'])
def predict():
    """Run predictions on patient report"""
    if 'patient_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    data = request.json
    report_data = data.get('report_data')
    
    if not report_data:
        return jsonify({'success': False, 'message': 'No report data provided'})
    
    try:
        # Run all predictions
        predictions = inference_engine.predict_all(report_data)
        
        # Get recommendations
        recommendations = get_all_recommendations(predictions)
        
        # Get summary message
        summary = get_summary_message(predictions)
        
        return jsonify({
            'success': True,
            'predictions': predictions,
            'recommendations': recommendations,
            'summary': summary
        })
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/patient/reports')
def get_patient_reports():
    """Get all patient reports"""
    if 'patient_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    patient_id = session['patient_id']
    patient_data = load_patient_data(patient_id)
    
    if not patient_data:
        return jsonify({'success': False, 'message': 'Patient not found'})
    
    return jsonify({
        'success': True,
        'reports': patient_data['reports']
    })

@app.route('/api/patient/history')
def get_patient_history():
    """Get patient history with predictions"""
    if 'patient_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    patient_id = session['patient_id']
    patient_data = load_patient_data(patient_id)
    
    if not patient_data:
        return jsonify({'success': False, 'message': 'Patient not found'})
    
    # Process all reports
    history = []
    for report in patient_data['reports']:
        predictions = inference_engine.predict_all(report)
        history.append({
            'date': report['date'],
            'report_id': report['report_id'],
            'predictions': predictions
        })
    
    return jsonify({
        'success': True,
        'history': history
    })

@app.route('/report/<report_id>')
def view_report(report_id):
    """View specific report"""
    if 'patient_id' not in session:
        return render_template('login.html')
    
    patient_id = session['patient_id']
    patient_data = load_patient_data(patient_id)
    
    if not patient_data:
        return "Patient not found", 404
    
    # Find the report
    report = None
    for r in patient_data['reports']:
        if r['report_id'] == report_id:
            report = r
            break
    
    if not report:
        return "Report not found", 404
    
    # Run predictions
    predictions = inference_engine.predict_all(report)
    recommendations = get_all_recommendations(predictions)
    summary = get_summary_message(predictions)
    
    return render_template('report.html',
                         patient=patient_data,
                         report=report,
                         predictions=predictions,
                         recommendations=recommendations,
                         summary=summary)


@app.route('/admin/patient/<patient_id>/report/<report_id>')
def admin_view_report(patient_id, report_id):
    """Admin view of a specific patient report (opens in new tab)."""
    if not session.get('is_admin'):
        return redirect(url_for('index'))

    # Reuse existing report view logic by setting the session patient_id
    session['patient_id'] = patient_id
    return redirect(url_for('view_report', report_id=report_id))

@app.route('/progress')
def progress():
    """Progress tracking page"""
    if 'patient_id' not in session:
        return render_template('login.html')
    
    patient_id = session['patient_id']
    patient_data = load_patient_data(patient_id)
    
    if not patient_data:
        return "Patient not found", 404
    
    return render_template('progress.html', patient=patient_data)


@app.route('/admin/patient/<patient_id>/analysis')
def admin_patient_analysis(patient_id):
    """Admin view of patient's progress/analysis (opens in new tab)."""
    if not session.get('is_admin'):
        return redirect(url_for('index'))

    # Point existing progress machinery at the selected patient
    session['patient_id'] = patient_id
    return redirect(url_for('progress'))

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')


@app.route('/contact')
def contact_page():
    """Simple contact redirect to home where contact modal exists."""
    # For now just send users back to the home page; contact info is in the portal modal
    return redirect(url_for('index'))

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("REHABSENSE WEB APPLICATION")
    print("=" * 60)
    print("\nStarting server...")
    print("Open your browser and go to: http://localhost:5000")
    print("\nTest Patients:")
    print("  - Patient A: Single report analysis")
    print("  - Patient B: Progress tracking (12 reports)")
    print("\n" + "=" * 60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)