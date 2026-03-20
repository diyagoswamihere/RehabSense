"""
RehabSense Backend Server
Flask application serving the rehabilitation monitoring portal
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import json
import os
import sys
from datetime import datetime

# Simple in-memory translation catalog (free, no paid API)
SUPPORTED_LANGUAGES = ['en', 'es', 'hi', 'bn', 'mr', 'ta', 'kn', 'te', 'or', 'pa', 'hry', 'gu', 'bho', 'ur']
LANGUAGE_LABELS = {
    'en': 'English',
    'es': 'Español',
    'hi': 'हिन्दी',
    'bn': 'বাংলা',
    'mr': 'मराठी',
    'ta': 'தமிழ்',
    'kn': 'ಕನ್ನಡ',
    'te': 'తెలుగు',
    'or': 'ଓଡ଼ିଆ',
    'pa': 'ਪੰਜਾਬੀ',
    'hry': 'हरियाणवी',
    'gu': 'ગુજરાતી',
    'bho': 'भोजपुरी',
    'ur': 'اردو'
}
DEFAULT_LANGUAGE = 'en'
TRANSLATIONS = {
    'en': {
        'app_name': 'RehabSense',
        'nav_home': 'Home',
        'nav_dashboard': 'Dashboard',
        'nav_progress': 'Progress',
        'nav_contact': 'Contact',
        'nav_logout': 'Logout',
        'nav_login': 'Login',
        'hero_title': 'RehabSense',
        'hero_tagline': 'Your smart Rehabilitation Assistant',
        'get_started': 'Get Started',
        'about_heading': 'About RehabSense',
        'login_options': 'Login Options',
        'login_as_patient': 'Login as Patient',
        'login_as_admin': 'Login as Administrator',
        'patient_id': 'Patient ID',
        'password': 'Password',
        'submit': 'Login',
        'invalid_credentials': 'Invalid patient ID or password.',
        'welcome': 'Welcome',
        'your_health_reports': 'Your Health Reports',
        'view_details': 'View Details',
        'view_progress': 'View Progress Over Time',
        'admin_dashboard': 'Admin Dashboard',
        'language': 'Language',
        'summary_heading': 'Overall Summary',
        'ai_analysis_results': 'AI Analysis Results',
        'heartbeat_analysis': 'Heartbeat Analysis',
        'blood_glucose': 'Blood Glucose',
        'breathing_pattern': 'Breathing Pattern',
        'speech_pattern': 'Speech Pattern',
        'emotional_state': 'Emotional State',
        'posture_analysis': 'Posture Analysis',
        'heart_rate': 'Heart Rate',
        'confidence': 'Confidence',
        'bmi': 'BMI',
        'rate': 'Rate',
        'sentiment_score': 'Sentiment Score',
        'posture_score': 'Posture Score',
        'personalized_recommendations': 'Personalized Recommendations',
        'exercises_activities': 'Exercises & Activities',
        'lifestyle_tips': 'Lifestyle Tips',
        'important_notes': 'Important Notes',
        'services': 'Services',
        'drop_mail': 'Drop mail',
        'ring_us': 'Ring us',
        'patient_login': 'Patient Login',
        'admin_login': 'Admin Login',
        'enter_patient_id': 'Enter Patient ID',
        'enter_admin_id': 'Enter Admin ID',
        'enter_password': 'Enter Password',
        'admin_id': 'Admin ID',
        'invalid_admin_credentials': 'Invalid admin credentials.',
        'total_reports': 'Total Reports',
        'tracking_period': 'Tracking Period',
        'weeks': 'weeks',
        'health_metrics_over_time': 'Health Metrics Over Time',
        'heart_rate_trend': 'Heart Rate Trend',
        'posture_score_progression': 'Posture Score Progression',
        'emotional_state_distribution': 'Emotional State Distribution',
        'breathing_pattern_status': 'Breathing Pattern Status',
        'loading_progress_data': 'Loading your progress data...',
        'ai_powered_rehab_system': 'AI-Powered Rehabilitation Monitoring System',
        'project_overview': 'Project Overview',
        'six_ai_models': 'Six AI Models',
        'heartbeat_abnormality_detector': 'Heartbeat Abnormality Detector',
        'data_collection': 'Data Collection',
        'patient_metrics_collected': 'Patient health metrics are collected through reports',
        'ai_analysis': 'AI Analysis',
        'six_models_analyze': 'Six trained machine learning models analyze the data',
        'insights_generation': 'Insights Generation',
        'health_status_predictions': 'System generates health status predictions',
        'recommendations_heading': 'Recommendations',
        'personalized_exercise_tips': 'Personalized exercises and lifestyle tips are provided',
        'welcome_admin': 'Welcome Admin',
        'patients': 'Patients',
        'add_patient': 'Add Patient',
        'add_new_patient': 'Add New Patient',
        'select_patient_hint': 'Select a patient from the left to view details and reports.',
        'name': 'Name',
        'age': 'Age',
        'gender': 'Gender',
        'address': 'Address',
        'phone': 'Phone',
        'email': 'Email',
        'save_patient': 'Save Patient',
        'add_report': 'Add Report',
        'upload_report': 'Upload Report',
        'upload_files_hint': 'You can upload files like CSV, DOCX, etc.',
        'upload_file': 'Upload File',
        'enter_data_manually': 'Enter Data Manually',
        'save_report': 'Save Report',
        'rr_variance': 'RR Interval Variance',
        'glucose_age': 'Glucose Age',
        'meal_timing': 'Meal Timing',
        'activity_level': 'Activity Level',
        'glucose_range': 'Glucose Range',
        'breath_depth': 'Breath Depth',
        'rest_vs_exercise': 'Rest vs Exercise',
        'speech_rate': 'Speech Rate',
        'pause_frequency': 'Pause Frequency',
        'pitch_variability': 'Pitch Variability',
        'text_sentiment': 'Text Sentiment',
        'voice_emotion': 'Voice Emotion',
        'facial_emotion': 'Facial Emotion',
        'head_tilt': 'Head Tilt',
        'shoulder_alignment': 'Shoulder Alignment',
        'spine_angle': 'Spine Angle',
        'id': 'ID',
    },
    'es': {
        'app_name': 'RehabSense',
        'nav_home': 'Inicio',
        'nav_dashboard': 'Panel',
        'nav_progress': 'Progreso',
        'nav_contact': 'Contacto',
        'nav_logout': 'Cerrar sesión',
        'nav_login': 'Iniciar sesión',
        'hero_title': 'RehabSense',
        'hero_tagline': 'Tu asistente de rehabilitación inteligente',
        'get_started': 'Comenzar',
        'about_heading': 'Acerca de RehabSense',
        'login_options': 'Opciones de inicio de sesión',
        'login_as_patient': 'Iniciar sesión como paciente',
        'login_as_admin': 'Iniciar sesión como administrador',
        'patient_id': 'ID de paciente',
        'password': 'Contraseña',
        'submit': 'Iniciar sesión',
        'invalid_credentials': 'ID de paciente o contraseña inválidos.',
        'welcome': 'Bienvenido',
        'your_health_reports': 'Tus informes de salud',
        'view_details': 'Ver detalles',
        'view_progress': 'Ver progreso con el tiempo',
        'admin_dashboard': 'Panel de administrador',
        'language': 'Idioma',
    },
    'hi': {
        'app_name': 'RehabSense',
        'nav_home': 'होम',
        'nav_dashboard': 'डैशबोर्ड',
        'nav_progress': 'प्रगति',
        'nav_contact': 'संपर्क',
        'nav_logout': 'लॉग आउट',
        'nav_login': 'लॉग इन',
        'hero_title': 'RehabSense',
        'hero_tagline': 'आपका स्मार्ट पुनर्वास सहायक',
        'get_started': 'शुरू करें',
        'about_heading': 'RehabSense के बारे में',
        'login_options': 'लॉगिन विकल्प',
        'login_as_patient': 'रोगी के रूप में लॉगिन करें',
        'login_as_admin': 'व्यवस्थापक के रूप में लॉगिन करें',
        'patient_id': 'रोगी आईडी',
        'password': 'पासवर्ड',
        'submit': 'लॉग इन',
        'invalid_credentials': 'अमान्य रोगी ID या पासवर्ड।',
        'welcome': 'स्वागत है',
        'your_health_reports': 'आपकी स्वास्थ्य रिपोर्ट',
        'view_details': 'विवरण देखें',
        'view_progress': 'समय के साथ प्रगति दिखाएं',
        'admin_dashboard': 'एडमिन डैशबोर्ड',
        'language': 'भाषा',
    },
    'bn': {
        'app_name': 'RehabSense', 'nav_home': 'হোম', 'nav_dashboard': 'ড্যাশবোর্ড', 'nav_progress': 'উন্নতি', 'nav_contact': 'যোগাযোগ', 'nav_logout': 'লগ আউট', 'nav_login': 'লগইন', 'hero_title': 'RehabSense', 'hero_tagline': 'আপনার স্মার্ট পুনর্বাসন সহায়ক', 'get_started': 'শুরু করুন', 'about_heading': 'RehabSense সম্পর্কে', 'login_options': 'লগইন অপশন', 'login_as_patient': 'রোগী হিসেবে লগইন', 'login_as_admin': 'অ্যাডমিন হিসেবে লগইন', 'patient_id': 'রোগীর আইডি', 'password': 'পাসওয়ার্ড', 'submit': 'লগইন', 'invalid_credentials': 'অবৈধ রোগী আইডি অথবা পাসওয়ার্ড।', 'welcome': 'স্বাগতম', 'your_health_reports': 'আপনার স্বাস্থ্য রিপোর্ট', 'view_details': 'বিস্তারিত দেখুন', 'view_progress': 'সময়ের সাথে উন্নতি দেখুন', 'admin_dashboard': 'অ্যাডমিন ড্যাশবোর্ড', 'language': 'ভাষা'
    },
    'mr': {
        'app_name': 'RehabSense', 'nav_home': 'होम', 'nav_dashboard': 'डॅशबोर्ड', 'nav_progress': 'प्रगती', 'nav_contact': 'संपर्क', 'nav_logout': 'बाहेर विचलित', 'nav_login': 'लॉगिन', 'hero_title': 'RehabSense', 'hero_tagline': 'तुमचा स्मार्ट पुनर्वसन सहाय्यक', 'get_started': 'सुरू करा', 'about_heading': 'RehabSense विषयी', 'login_options': 'लॉगिन पर्याय', 'login_as_patient': 'रुग्ण म्हणून लॉगिन', 'login_as_admin': 'प्रशासक म्हणून लॉगिन', 'patient_id': 'रुग्ण आयडी', 'password': 'पासवर्ड', 'submit': 'लॉगिन', 'invalid_credentials': 'अवैध रुग्ण आयडी किंवा पासवर्ड.', 'welcome': 'स्वागत आहे', 'your_health_reports': 'आपल्या आरोग्य अहवाल', 'view_details': 'तपशील पहा', 'view_progress': 'कालांतराने प्रगती पहा', 'admin_dashboard': 'अॅडमिन डॅशबोर्ड', 'language': 'भाषा'
    },
    'ta': {
        'app_name': 'RehabSense', 'nav_home': 'முகப்பு', 'nav_dashboard': 'டேஷ்போர்டு', 'nav_progress': 'முன்னேற்றம்', 'nav_contact': 'தொடர்பு', 'nav_logout': 'வெளியேறு', 'nav_login': 'உள்நுழைக', 'hero_title': 'RehabSense', 'hero_tagline': 'உங்கள் நுண்ணறிவு மறுவடிவமைப்பு உதவியாளர்', 'get_started': 'தொடங்கு', 'about_heading': 'RehabSense பற்றி', 'login_options': 'உள்நுழைய விருப்பங்கள்', 'login_as_patient': 'நோயாளியாக உள்நுழைய', 'login_as_admin': 'நிர்வாகியாக உள்நுழைய', 'patient_id': 'நோயாளி ஐடி', 'password': 'கடவுச்சொல்', 'submit': 'உள்நுழைய', 'invalid_credentials': 'தவறான நோயாளி ஐடி அல்லது கடவுச்சொல்.', 'welcome': 'வா', 'your_health_reports': 'உங்கள் உடல்நிலை அறிக்கைகள்', 'view_details': 'விவரங்களை காண்க', 'view_progress': 'நேரத்தைக் குறித்து முன்னேற்றம் பாருங்கள்', 'admin_dashboard': 'நிர்வாக டேஷ்போர்டு', 'language': 'மொழி'
    },
    'kn': {
        'app_name': 'RehabSense', 'nav_home': 'ಮುಖಪುಟ', 'nav_dashboard': 'ಡ್ಯಾಶ್‌ಬೋರ್ಡ್', 'nav_progress': 'ಪ್ರಗತಿ', 'nav_contact': 'ಸಂಪರ್ಕ', 'nav_logout': 'ಲಾಗ್ ಔಟ್', 'nav_login': 'ಲಾಗಿನ್', 'hero_title': 'RehabSense', 'hero_tagline': 'ನಿಮ್ಮ ಸ್ಮಾರ್ಟ್ ಪುನರ್ವಸನ ಸಹಾಯಕ', 'get_started': 'ಆರಂಭಿಸಿ', 'about_heading': 'RehabSense ಬಗ್ಗೆ', 'login_options': 'ಲಾಗಿನ್ ಆಯ್ಕೆಗಳು', 'login_as_patient': 'ರೋಗಿಯಾಗಿಯಾಗಿ ಲಾಗಿನ್ ಮಾಡಿ', 'login_as_admin': 'ನಿರ್ವಹಣೆಗಾರನಾಗಿ ಲಾಗಿನ್ ಮಾಡಿ', 'patient_id': 'ರೋಗಿ ಐಡಿ', 'password': 'ಗೂಪ್ತ ಸೀಟು', 'submit': 'ಲಾಗಿನ್', 'invalid_credentials': 'ಅಮಾನ್ಯ ರೋಗಿ ಐಡಿ ಅಥವಾ ಪರವಾನಗಿ.', 'welcome': 'ಸ್ವಾಗತ', 'your_health_reports': 'ನಿಮ್ಮ ಆರೋಗ್ಯ ವರದಿಗಳು', 'view_details': 'ವಿವರಗಳನ್ನು ನೋಡಿ', 'view_progress': 'ಕಾಲಕಾಲಕ್ಕೆ ಪ್ರಗತಿಯನ್ನು ನೋಡಿ', 'admin_dashboard': 'ಅಡ್ಮಿನ್ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್', 'language': 'ಭಾಷೆ'
    },
    'te': {
        'app_name': 'RehabSense', 'nav_home': 'హోమ్', 'nav_dashboard': 'డాష్‌బోర్డు', 'nav_progress': 'పురోగతి', 'nav_contact': 'సంప్రదించండి', 'nav_logout': 'లాగౌట్', 'nav_login': 'లాగిన్', 'hero_title': 'RehabSense', 'hero_tagline': 'మీ స్మార్ట్ పునరుద్ధరణ సహాయకుడు', 'get_started': 'ప్రారంభించండి', 'about_heading': 'RehabSense గురించి', 'login_options': 'లాగిన్ ఎంపికలు', 'login_as_patient': 'రోగిగా లాగిన్', 'login_as_admin': 'నిర్వాహకుడిగా లాగిన్', 'patient_id': 'రోగి ఐడీ', 'password': 'పాస్వర్డ్', 'submit': 'లాగిన్', 'invalid_credentials': 'చెల్లని రోగి ఐడి లేదా పాస్వర్డ్.', 'welcome': 'స్వాగతం', 'your_health_reports': 'మీ ఆరోగ్య నివేదికలు', 'view_details': 'వివరాలు చూడండి', 'view_progress': 'సమయానుసారం పురోగతిని చూడండి', 'admin_dashboard': 'అడ్మిన్ డ్యాష్‌బోర్డు', 'language': 'భాష'
    },
    'or': {
        'app_name': 'RehabSense', 'nav_home': 'ହୋମ୍', 'nav_dashboard': 'ଡ୍ୟାଶବୋର୍ଡ', 'nav_progress': 'ପ୍ରଗତି', 'nav_contact': 'ସମ୍ପର୍କ', 'nav_logout': 'ଲଗ୍ ଆଉଟ୍', 'nav_login': 'ଲଗ୍ଇନ୍', 'hero_title': 'RehabSense', 'hero_tagline': 'ଆପଣଙ୍କର ସ୍ମାର୍ଟ ପୁନଃସଂରଚନା ସହାୟକ', 'get_started': 'ଆରମ୍ଭ କରନ୍ତୁ', 'about_heading': 'RehabSense ବିଷୟରେ', 'login_options': 'ଲଗ୍ଇନ୍ ବିକଳ୍ପ', 'login_as_patient': 'ରୋଗୀ ଭାବେ ଲଗ୍ଇନ୍', 'login_as_admin': 'ନିୟମକ ଭାବେ ଲଗ୍ଇନ୍', 'patient_id': 'ରୋଗୀ ଆଇଡି', 'password': 'ପাসୱାର୍ଡ', 'submit': 'ଲଗ୍ଇନ୍', 'invalid_credentials': 'ଅବୈଧ ରୋଗୀ ଆଇଡି କିମ୍ବା ପାସୱାର୍ଡ.', 'welcome': 'ସ୍ୱାଗତ', 'your_health_reports': 'ଆପଣଙ୍କର ସ୍ୱାସ୍ଥ୍ୟ ରିପୋର୍ଟ', 'view_details': 'ବିବରଣୀ ଦେଖନ୍ତୁ', 'view_progress': 'ସମୟ ସହ ଉନ୍ନତି ଦେଖନ୍ତୁ', 'admin_dashboard': 'ଅଡ୍ମିନ୍ ଡ୍ୟାଶବୋର୍ଡ', 'language': 'ଭାଷା'
    },
    'pa': {
        'app_name': 'RehabSense', 'nav_home': 'ਹੋਮ', 'nav_dashboard': 'ਡੈਸ਼ਬੋਰਡ', 'nav_progress': 'ਪ੍ਰਗਤੀ', 'nav_contact': 'ਸੰਪਰਕ', 'nav_logout': 'ਲਾਗ ਆਊਟ', 'nav_login': 'ਲਾਗਿਨ', 'hero_title': 'RehabSense', 'hero_tagline': 'ਤੁਹਾਡਾ ਸਮਾਰਟ ਪੁਨਰਵਾਸ ਸਹਾਇਕ', 'get_started': 'ਸ਼ੁਰੂ ਕਰੋ', 'about_heading': 'RehabSense ਬਾਰੇ', 'login_options': 'ਲਾਗਿਨ ਵਿਕਲਪ', 'login_as_patient': 'ਰੋਗੀ ਵਜੋਂ ਲਾਗਿਨ', 'login_as_admin': 'ਐਡਮਿਨ ਵਜੋਂ ਲਾਗਿਨ', 'patient_id': 'ਰੋਗੀ ਆਈਡੀ', 'password': 'ਪਾਸਵਰਡ', 'submit': 'ਲਾਗਿਨ', 'invalid_credentials': 'ਗਲਤ ਰੋਗੀ ਆਈਡੀ ਜਾਂ ਪਾਸਵਰਡ.', 'welcome': 'ਸਤ ਸ੍ਰੀ ਅਕਾਲ', 'your_health_reports': 'ਤੁਹਾਡੇ ਸਿਹਤ ਰਿਪੋਰਟ', 'view_details': 'ਵੇਰਵੇ ਵੇਖੋ', 'view_progress': 'ਸਮੇਂ ਨਾਲ ਪ੍ਰਗਤੀ ਵੇਖੋ', 'admin_dashboard': 'ਐਡਮਿਨ ਡੈਸ਼ਬੋਰਡ', 'language': 'ਭਾਸ਼ਾ'
    },
    'hry': {
        'app_name': 'RehabSense', 'nav_home': 'होम', 'nav_dashboard': 'डैशबोर्ड', 'nav_progress': 'प्रगति', 'nav_contact': 'संपर्क', 'nav_logout': 'लॉग आउट', 'nav_login': 'लॉग इन', 'hero_title': 'RehabSense', 'hero_tagline': 'तुम्हारा स्मार्ट रीहैब सहायक', 'get_started': 'शुरू कर', 'about_heading': 'RehabSense के बारे में', 'login_options': 'लॉगिन विकल्प', 'login_as_patient': 'मरीज के रूप में लॉगिन', 'login_as_admin': 'एडमिन के रूप में लॉगिन', 'patient_id': 'मरीज आईडी', 'password': 'पासवर्ड', 'submit': 'लॉग इन', 'invalid_credentials': 'गलत मरीज आईडी या पासवर्ड।', 'welcome': 'स्वागत से', 'your_health_reports': 'तेरी हेल्थ रिपोर्ट', 'view_details': 'डिटेल देख', 'view_progress': 'टाइम के साथ प्रगति देख', 'admin_dashboard': 'एडमिन डैशबोर्ड', 'language': 'भाषा'
    },
    'gu': {
        'app_name': 'RehabSense', 'nav_home': 'હોમ', 'nav_dashboard': 'ડેશબોર્ડ', 'nav_progress': 'પ્રગતિ', 'nav_contact': 'સંપર્ક', 'nav_logout': 'લોગ આઉટ', 'nav_login': 'લોગિન', 'hero_title': 'RehabSense', 'hero_tagline': 'તમારો સ્માર્ટ પુનર્વસન સહાયક', 'get_started': 'પ્રારંભ કરો', 'about_heading': 'RehabSense વિશે', 'login_options': 'લોગિન વિકલ્પો', 'login_as_patient': 'રોગી તરીકે લોગિન', 'login_as_admin': 'એડમિન તરીકે લોગિન', 'patient_id': 'રોગી આઈડી', 'password': 'પાસવર્ડ', 'submit': 'લોગિન', 'invalid_credentials': 'અમાન્ય રોગી આઈડી અથવા પાસવર્ડ.', 'welcome': 'સ્વાગત છે', 'your_health_reports': 'તમારી આરોગ્ય રિપોર્ટ્સ', 'view_details': 'વિગતો જુઓ', 'view_progress': 'સમય સાથે પ્રગતિ જુઓ', 'admin_dashboard': 'એડમિન ડેશબોર્ડ', 'language': 'ભાષા'
    },
    'bho': {
        'app_name': 'RehabSense', 'nav_home': 'होम', 'nav_dashboard': 'डैशबोर्ड', 'nav_progress': 'प्रगति', 'nav_contact': 'संपर्क', 'nav_logout': 'लॉग आउट', 'nav_login': 'लॉगिन', 'hero_title': 'RehabSense', 'hero_tagline': 'तोहार स्मार्ट पुनरावास सहायक', 'get_started': 'शुरू कर', 'about_heading': 'RehabSense के बारे में', 'login_options': 'लॉगिन विकल्प', 'login_as_patient': 'मरीज के रूप में लॉगिन', 'login_as_admin': 'एडमिन के रूप में लॉगिन', 'patient_id': 'मरीज आईडी', 'password': 'पासवर्ड', 'submit': 'लॉगिन', 'invalid_credentials': 'गलत मरीज आईडी या पासवर्ड।', 'welcome': 'स्वागत बा', 'your_health_reports': 'तोहार स्वास्थ्य रिपोर्ट', 'view_details': 'विवरण देखें', 'view_progress': 'समय के साथ प्रगति देखें', 'admin_dashboard': 'एडमिन डैशबोर्ड', 'language': 'भाषा'
    },
    'ur': {
        'app_name': 'RehabSense', 'nav_home': 'ہوم', 'nav_dashboard': 'ڈیش بورڈ', 'nav_progress': 'پیش رفت', 'nav_contact': 'رابطہ', 'nav_logout': 'لاگ آؤٹ', 'nav_login': 'لاگ ان', 'hero_title': 'RehabSense', 'hero_tagline': 'آپ کا اسمارٹ ریہیب معاون', 'get_started': 'شروع کریں', 'about_heading': 'RehabSense کے بارے میں', 'login_options': 'لاگ ان کے اختیارات', 'login_as_patient': 'مریض کے طور پر لاگ ان کریں', 'login_as_admin': 'ایڈمن کے طور پر لاگ ان کریں', 'patient_id': 'مریض شناخت', 'password': 'پاس ورڈ', 'submit': 'لاگ ان', 'invalid_credentials': 'غلط مریض شناخت یا پاس ورڈ۔', 'welcome': 'خوش آمدید', 'your_health_reports': 'آپ کی صحت کی رپورٹس', 'view_details': 'تفصیلات دیکھیں', 'view_progress': 'وقت کے ساتھ پیش رفت دیکھیں', 'admin_dashboard': 'ایڈمن ڈیش بورڈ', 'language': 'زبان'
    }
}

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

@app.context_processor
def inject_i18n_context():
    def t(key):
        lang = session.get('lang') if session.get('lang') in SUPPORTED_LANGUAGES else request.accept_languages.best_match(SUPPORTED_LANGUAGES) or DEFAULT_LANGUAGE
        return TRANSLATIONS.get(lang, TRANSLATIONS[DEFAULT_LANGUAGE]).get(key, TRANSLATIONS[DEFAULT_LANGUAGE].get(key, key))
    return {
        't': t,
        'current_lang': session.get('lang', request.accept_languages.best_match(SUPPORTED_LANGUAGES) or DEFAULT_LANGUAGE),
        'supported_languages': SUPPORTED_LANGUAGES,
        'language_labels': LANGUAGE_LABELS
    }

@app.route('/set_language/<lang>')
def set_language(lang):
    if lang not in SUPPORTED_LANGUAGES:
        lang = DEFAULT_LANGUAGE
    session['lang'] = lang
    return redirect(request.referrer or url_for('index'))

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
    
    return jsonify({'success': False, 'message': TRANSLATIONS.get(session.get('lang', DEFAULT_LANGUAGE), TRANSLATIONS[DEFAULT_LANGUAGE]).get('invalid_credentials', 'Invalid patient ID or password.')})

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

    return jsonify({'success': False, 'message': TRANSLATIONS.get(session.get('lang', DEFAULT_LANGUAGE), TRANSLATIONS[DEFAULT_LANGUAGE]).get('invalid_admin_credentials', 'Invalid admin credentials.')})


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
    
    # Get current language from session
    current_lang = session.get('lang', DEFAULT_LANGUAGE)
    
    # Run predictions
    predictions = inference_engine.predict_all(report)
    recommendations = get_all_recommendations(predictions, current_lang)
    summary = get_summary_message(predictions, current_lang)
    
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