"""
RehabSense Backend Server
Flask application serving the rehabilitation monitoring portal
"""

from flask import Flask, render_template, request, jsonify, session
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


def load_patient_data(patient_id):
    """Load patient data from JSON file"""
    # Map new patient IDs to old file names
    file_mapping = {
        '1D55PL6': 'patient_A.json',
        '7D42PL2': 'patient_B.json'
    }
    
    filename = file_mapping.get(patient_id, f'patient_{patient_id}.json')
    filepath = os.path.join(DATA_DIR, 'patients', filename)
    
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    return None

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
    return jsonify({'success': True})

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

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

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