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
        'please_select_patient_first': 'Please select a patient first.',
        'please_choose_file': 'Please choose a file.',
        'failed_add_patient': 'Failed to add patient.',
        'failed_upload_report': 'Failed to upload report.',
        'failed_save_report': 'Failed to save report.',
        'view_analysis': 'View Analysis',
        'reports_heading': 'Reports',
        'no_reports_yet_patient': 'No reports yet for this patient.',
        'login_failed_try_again': 'Login failed. Please try again.',
        'error_logging_in': 'Error logging in. Please try again.',
        'admin_login_failed_try_again': 'Admin login failed. Please try again.',
        'error_logging_in_admin': 'Error logging in as admin. Please try again.',
        'score_0_100': 'Score (0-100)',
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
        # About section
        'about_para1': 'Rehabilitation patients often need continuous, multi-parameter monitoring to ensure steady recovery and to detect complications at an early stage. However, most existing solutions address only a single aspect of health such as heart rate, posture, or glucose levels, resulting in fragmented care. Patients are often forced to juggle multiple devices and applications, creating unnecessary complexity and reducing long-term engagement. This gap is especially critical for individuals recovering from cardiovascular, respiratory, musculoskeletal, metabolic, or stress-related conditions.',
        'about_para2': 'RehabSense is designed to bridge this gap through a unified, intelligent, multi-modal health monitoring platform. It integrates analysis of key health indicators, including heartbeat irregularities, estimated blood glucose trends, breathing patterns, speech characteristics, emotional state, and posture, into a single cohesive system.',
        'about_para3': 'A core feature of RehabSense is its real-time, video-based posture detection, which enables accurate tracking of body alignment and movement without need for specialized hardware. Each component is lightweight, modular, and scalable, allowing for phased development and seamless integration.',
        'about_para4': 'The platform also provides a user-friendly web interface where patients can log health data, access historical records, and visualize progress through intuitive analytics. By consolidating multiple monitoring capabilities into one intelligent assistant, RehabSense enhances patient engagement, supports personalized rehabilitation plans, and delivers actionable insights for clinicians, making long-term recovery more structured, informed, and accessible.',
        # Services section
        'service1_title': 'Get Real-time Diagnosis',
        'service1_desc': 'Experience instant health analysis with interactive charts and comprehensive abnormality detection through our advanced AI-powered monitoring system.',
        'service2_title': 'Great Visuals and Charts',
        'service2_desc': 'Understand your health insights beautifully with intuitive visualizations and track your rehabilitation progress with comprehensive, easy-to-read charts.',
        'service3_title': 'Real-time Recommendations',
        'service3_desc': 'Receive personalized exercise routines, dietary guidance, and doctor suggestions tailored to your specific health condition and recovery goals.',
        'service4_title': 'Multilingual Support',
        'service4_desc': 'Access our platform in your preferred language with comprehensive multilingual support, making healthcare accessible to everyone regardless of language barriers.',
        'our_services': 'Our Services',
        # Footer
        'educational_prototype': 'Educational Prototype Only',
        'disclaimer': 'This system is for demonstration purposes and does not provide medical advice. Always consult qualified healthcare professionals for medical decisions.',
        'copyright': '© 2026 RehabSense - AI Rehabilitation Monitoring System',
        # Prediction status labels
        'status_normal': 'Normal',
        'status_bradycardia': 'Bradycardia',
        'status_tachycardia': 'Tachycardia',
        'status_irregular': 'Irregular',
        'status_low': 'Low',
        'status_high': 'High',
        'status_shallow_breathing': 'Shallow Breathing',
        'status_apnea_risk': 'Apnea Risk',
        'status_normal_speech': 'Normal Speech',
        'status_slurred_speech': 'Slurred/Slow',
        'status_stressed_speech': 'Stressed Speech',
        'status_happy': 'Happy',
        'status_neutral': 'Neutral',
        'status_stressed': 'Stressed',
        'status_sad': 'Sad',
        'status_good_posture': 'Good Posture',
        'status_forward_head': 'Forward Head Posture',
        'status_slouched': 'Slouched Sitting',
        'bpm': 'bpm',
        'breathing_rate': 'Breathing Rate',
        'breaths_per_min': 'breaths/min',
        'words_per_min': 'words/min',
        'out_of_100': '/100',
        'report_title': 'Report',
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
        'about_para1': 'Los pacientes en rehabilitación a menudo necesitan monitoreo continuo de múltiples parámetros para garantizar una recuperación estable y detectar complicaciones en una etapa temprana. Sin embargo, la mayoría de las soluciones existentes abordan solo un aspecto de la salud como la frecuencia cardíaca, la postura o los niveles de glucosa, resultando en una atención fragmentada. Los pacientes a menudo se ven obligados a usar múltiples dispositivos y aplicaciones, creando complejidad innecesaria y reduciendo el compromiso a largo plazo.',
        'about_para2': 'RehabSense está diseñado para cerrar esta brecha a través de una plataforma de monitoreo de salud multimodal unificada e inteligente. Integra el análisis de indicadores de salud clave, incluidas irregularidades cardíacas, tendencias estimadas de glucosa en sangre, patrones de respiración, características del habla, estado emocional y postura, en un sistema cohesivo.',
        'about_para3': 'Una característica principal de RehabSense es su detección de postura basada en video en tiempo real, que permite un seguimiento preciso de la alineación y el movimiento del cuerpo sin necesidad de hardware especializado. Cada componente es liviano, modular y escalable, permitiendo desarrollo por fases eintegración sin problemas.',
        'about_para4': 'La plataforma también proporciona una interfaz web amigable donde los pacientes pueden registrar datos de salud, acceder a registros históricos y visualizar el progreso a través de análisis intuitivos. Al consolidar múltiples capacidades de monitoreo en un asistente inteligente, RehabSense mejora el compromiso del paciente, apoya planes de rehabilitación personalizados y ofrece información procesable para clínicos.',
        'service1_title': 'Obtener Diagnóstico en Tiempo Real',
        'service1_desc': 'Experimente análisis de salud instantáneo con gráficos interactivos y detección completa de anomalías a través de nuestro sistema de monitoreo avanzado impulsado por IA.',
        'service2_title': 'Excelentes Visuales y Gráficos',
        'service2_desc': 'Comprenda sus conocimientos de salud hermosamente con visualizaciones intuitivas y realice un seguimiento de su progreso de rehabilitación con gráficos completos y fáciles de leer.',
        'service3_title': 'Recomendaciones en Tiempo Real',
        'service3_desc': 'Reciba rutinas de ejercicio personalizadas, orientación dietética y sugerencias médicas adaptadas a su condición de salud específica y objetivos de recuperación.',
        'service4_title': 'Soporte Multilingüe',
        'service4_desc': 'Acceda a nuestra plataforma en su idioma preferido con soporte multilingüe integral, haciendo que la atención médica sea accesible para todos independientemente de las barreras del idioma.',
        'our_services': 'Nuestros Servicios',
        'educational_prototype': 'Prototipo Educativo Únicamente',
        'disclaimer': 'Este sistema es solo para fines de demostración y no proporciona asesoramiento médico. Siempre consulte profesionales de salud calificados para decisiones médicas.',
        'copyright': '© 2026 RehabSense - Sistema de Monitoreo de Rehabilitación Impulsado por IA',
        'status_normal': 'Normal',
        'status_bradycardia': 'Bradicardia',
        'status_tachycardia': 'Taquicardia',
        'status_irregular': 'Irregular',
        'status_low': 'Bajo',
        'status_high': 'Alto',
        'status_shallow_breathing': 'Respiración Superficial',
        'status_apnea_risk': 'Riesgo de Apnea',
        'status_normal_speech': 'Habla Normal',
        'status_slurred_speech': 'Habla Arrastrada/Lenta',
        'status_stressed_speech': 'Habla Estresada',
        'status_happy': 'Feliz',
        'status_neutral': 'Neutral',
        'status_stressed': 'Estresado',
        'status_sad': 'Triste',
        'status_good_posture': 'Buena Postura',
        'status_forward_head': 'Postura con Cabeza Adelante',
        'status_slouched': 'Sentado Encorvado',
        'exercises_activities': 'Ejercicios y Actividades',
        'lifestyle_tips': 'Consejos de Estilo de Vida',
        'important_notes': 'Notas Importantes',
        'bpm': 'ppm',
        'breaths_per_min': 'respiraciones/min',
        'words_per_min': 'palabras/min',
        'out_of_100': '/100',
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
        'summary_heading': 'समग्र सारांश',
        'ai_analysis_results': 'एआई विश्लेषण परिणाम',
        'heartbeat_analysis': 'हृदय धड़कन विश्लेषण',
        'blood_glucose': 'रक्त शर्करा',
        'breathing_pattern': 'श्वसन पैटर्न',
        'speech_pattern': 'भाषण पैटर्न',
        'emotional_state': 'भावनात्मक स्थिति',
        'posture_analysis': 'मुद्रा विश्लेषण',
        'heart_rate': 'हृदय गति',
        'confidence': 'विश्वसनीयता',
        'bmi': 'बीएमआई',
        'rate': 'दर',
        'sentiment_score': 'भावना स्कोर',
        'posture_score': 'मुद्रा स्कोर',
        'personalized_recommendations': 'व्यक्तिगत सिफारिशें',
        'exercises_activities': 'व्यायाम और गतिविधियां',
        'lifestyle_tips': 'जीवनशैली सुझाव',
        'important_notes': 'महत्वपूर्ण नोट्स',
        'about_para1': 'पुनर्वास रोगियों को अक्सर निरंतर, बहु-पैरामीटर निगरानी की आवश्यकता होती है ताकि स्थिर रिकवरी सुनिश्चित हो सके और जल्दी स्टेज में जटिलताओं का पता चल सके। हालांकि, अधिकांश मौजूदा समाधान स्वास्थ्य के केवल एक पहलू को संबोधित करते हैं जैसे हृदय गति, मुद्रा, या ग्लूकोज स्तर, जिससे विखंडित देखभाल होती है।',
        'about_para2': 'RehabSense एक एकीकृत, बुद्धिमान, बहु-मोडल स्वास्थ्य निगरानी प्लेटफॉर्म के माध्यम से इस अंतर को पाटने के लिए डिज़ाइन किया गया है। यह हृदय गति अनियमितताओं, अनुमानित रक्त शर्करा के रुझानों, श्वसन पैटर्न, भाषण विशेषताओं, भावनात्मक स्थिति और मुद्रा सहित मुख्य स्वास्थ्य संकेतकों का विश्लेषण एकीकृत करता है।',
        'about_para3': 'RehabSense की मुख्य विशेषता इसकी रीयल-टाइम, वीडियो-आधारित मुद्रा पहचान है, जो विशेष हार्डवेयर की आवश्यकता के बिना शरीर के संरेखण और गति की सटीक ट्रैकिंग सक्षम करती है।',
        'about_para4': 'प्लेटफॉर्म एक उपयोगकर्ता-अनुकूल वेब इंटरफेस भी प्रदान करता है जहां रोगी स्वास्थ्य डेटा लॉग कर सकते हैं, ऐतिहासिक रिकॉर्ड तक पहुंच सकते हैं, और सहज विश्लेषण के माध्यम से प्रगति की कल्पना कर सकते हैं।',
        'service1_title': 'रीयल-टाइम निदान प्राप्त करें',
        'service1_desc': 'इंटरेक्टिव चार्ट और हमारी उन्नत AI-संचालित निगरान प्रणाली के माध्यम से व्यापक विसंगति पहचान के साथ तत्काल स्वास्थ्य विश्लेषण का अनुभव लें।',
        'service2_title': 'बेहतरीन विजुअल और चार्ट',
        'service2_desc': 'सहज दृश्य के साथ अपनी स्वास्थ्य अंतर्दृष्टि को सुंदरता से समझें और व्यापक, आसानी से पढ़े जाने वाले चार्ट के साथ अपनी पुनर्वास प्रगति को ट्रैक करें।',
        'service3_title': 'रीयल-टाइम सिफारिशें',
        'service3_desc': 'आपकी विशिष्ट स्वास्थ्य स्थिति और रिकवरी लक्ष्यों के अनुरूप व्यक्तिगत व्यायाम दिनचर्या, आहार संबंधी मार्गदर्शन और डॉक्टर की सिफारिशें प्राप्त करें।',
        'service4_title': 'बहुभाषी समर्थन',
        'service4_desc': 'अपनी पसंदीदा भाषा में हमारे प्लेटफॉर्म तक पहुंचें व्यापक बहुभाषी समर्थन के साथ, जो भाषा बाधाओं के बावजूद स्वास्थ्यसेवा को सभी के लिए सुलभ बनाता है।',
        'our_services': 'हमारी सेवाएं',
        'educational_prototype': 'केवल शैक्षणिक प्रोटोटाइप',
        'disclaimer': 'यह सिस्टम केवल प्रदर्शन उद्देश्यों के लिए है और चिकित्सा सलाह प्रदान नहीं करता है। चिकित्सा निर्णयों के लिए हमेश योग्य स्वास्थ्यसेवा पेशेवरों से परामर्श लें।',
        'copyright': '© 2026 RehabSense - AI पुनर्वास निगरानी प्रणाली',
        'status_normal': 'सामान्य',
        'status_bradycardia': 'धीमी हृदय गति',
        'status_tachycardia': 'तेज हृदय गति',
        'status_irregular': 'अनियमित',
        'status_low': 'कम',
        'status_high': 'उच्च',
        'status_shallow_breathing': 'उथली सांस',
        'status_apnea_risk': 'एपनिया जोखिम',
        'status_normal_speech': 'सामान्य भाषण',
        'status_slurred_speech': 'गड़बड़ाता/धीमा',
        'status_stressed_speech': 'तनावपूर्ण भाषण',
        'status_happy': 'खुश',
        'status_neutral': 'तटस्थ',
        'status_stressed': 'तनावग्रस्त',
        'status_sad': 'उदास',
        'status_good_posture': 'अच्छी मुद्रा',
        'status_forward_head': 'आगे की ओर सिर की मुद्रा',
        'status_slouched': 'झुकी हुई बैठक',
        'exercises_activities': 'व्यायाम और गतिविधियां',
        'lifestyle_tips': 'जीवनशैली टिप्स',
        'important_notes': 'महत्वपूर्ण नोट्स',
        'bpm': 'bpm',
        'breaths_per_min': 'साँसें/मिनिट',
        'words_per_min': 'शब्द/मिनिट',
        'out_of_100': '/100',
    },
    'bn': {
        'app_name': 'RehabSense',
        'nav_home': 'হোম',
        'nav_dashboard': 'ড্যাশবোর্ড',
        'nav_progress': 'উন্নতি',
        'nav_contact': 'যোগাযোগ',
        'nav_logout': 'লগ আউট',
        'nav_login': 'লগইন',
        'hero_title': 'RehabSense',
        'hero_tagline': 'আপনার স্মার্ট পুনর্বাসন সহায়ক',
        'get_started': 'শুরু করুন',
        'about_heading': 'RehabSense সম্পর্কে',
        'login_options': 'লগইন অপশন',
        'login_as_patient': 'রোগী হিসেবে লগইন',
        'login_as_admin': 'অ্যাডমিন হিসেবে লগইন',
        'patient_id': 'রোগীর আইডি',
        'password': 'পাসওয়ার্ড',
        'submit': 'লগইন',
        'invalid_credentials': 'অবৈধ রোগী আইডি অথবা পাসওয়ার্ড।',
        'welcome': 'স্বাগতম',
        'your_health_reports': 'আপনার স্বাস্থ্য রিপোর্ট',
        'view_details': 'বিস্তারিত দেখুন',
        'view_progress': 'সময়ের সাথে উন্নতি দেখুন',
        'admin_dashboard': 'অ্যাডমিন ড্যাশবোর্ড',
        'language': 'ভাষা',
        'summary_heading': 'সামগ্রিক সারসংক্ষেপ',
        'ai_analysis_results': 'এআই বিশ্লেষণ ফলাফল',
        'heartbeat_analysis': 'হৃদস্পন্দন বিশ্লেষণ',
        'blood_glucose': 'রক্ত গ্লুকোজ',
        'breathing_pattern': 'শ্বাসের প্যাটার্ন',
        'speech_pattern': 'কথার প্যাটার্ন',
        'emotional_state': 'আবেগের অবস্থা',
        'posture_analysis': 'মুদ্রা বিশ্লেষণ',
        'heart_rate': 'হৃদস্পন্দন',
        'confidence': 'আত্মবিশ্বাস',
        'bmi': 'বিএমআই',
        'rate': 'হার',
        'sentiment_score': 'অনুভূতি স্কোর',
        'posture_score': 'মুদ্রা স্কোর',
        'personalized_recommendations': 'ব্যক্তিগতকৃত সুপারিশ',
        'exercises_activities': 'ব্যায়াম ও কার্যক্রম',
        'lifestyle_tips': 'জীবনধারার টিপস',
        'important_notes': 'গুরুত্বপূর্ণ নোট',
        'services': 'সেবা',
        'drop_mail': 'ইমেইল পাঠান',
        'ring_us': 'আমাদের যোগাযোগ করুন',
        'patient_login': 'রোগী লগইন',
        'admin_login': 'অ্যাডমিন লগইন',
        'enter_patient_id': 'রোগী আইডি প্রবেश করুন',
        'enter_admin_id': 'অ্যাডমিন আইডি প্রবেश করুন',
        'enter_password': 'পাসওয়ার্ড প্রবেশ করুন',
        'admin_id': 'অ্যাডমিন আইডি',
        'invalid_admin_credentials': 'অবৈধ অ্যাডমিন শংসাপত্র।',
        'total_reports': 'মোট রিপোর্ট',
        'tracking_period': 'ট্র্যাকিং সময়কাল',
        'weeks': 'সপ্তাহ',
        'health_metrics_over_time': 'সময়ের সাথে স্বাস্থ্য মেট্রিক্স',
        'heart_rate_trend': 'হৃদস্পন্দন প্রবণতা',
        'posture_score_progression': 'মুদ্রা স্কোর অগ্রগতি',
        'emotional_state_distribution': 'আবেগের অবস্থা বিতরণ',
        'breathing_pattern_status': 'শ্বাসের প্যাটার্ন স্ট্যাটাস',
        'loading_progress_data': 'আপনার অগ্রগতি ডেটা লোড হচ্ছে...',
        'ai_powered_rehab_system': 'এআই-চালিত পুনর্বাসন পর্যবেক্ষণ সিস্টেম',
        'project_overview': 'প্রকল্প সংক্ষিপ্তসার',
        'six_ai_models': 'ছয়টি এআই মডেল',
        'heartbeat_abnormality_detector': 'হৃদস্পন্দন অস্বাভাবিকতা সনাক্তকরণ',
        'data_collection': 'ডেটা সংগ্রহ',
        'patient_metrics_collected': 'রোগীর স্বাস্থ্য মেট্রিক্স রিপোর্টের মাধ্যমে সংগ্রহ করা হয়',
        'ai_analysis': 'এআই বিশ্লেষণ',
        'six_models_analyze': 'ছয়টি প্রশিক্ষিত মেশিন লার্নিং মডেল ডেটা বিশ্লেষণ করে',
        'insights_generation': 'অন্তর্দৃষ্টি উৎপাদন',
        'health_status_predictions': 'সিস্টেম স্বাস্থ্য অবস্থার পূর্বাভাস তৈরি করে',
        'recommendations_heading': 'সুপারিশ',
        'personalized_exercise_tips': 'ব্যক্তিগত ব্যায়াম এবং জীবনধারা টিপস প্রদান করা হয়',
        'welcome_admin': 'অ্যাডমিনকে স্বাগতম',
        'patients': 'রোগী',
        'add_patient': 'রোগী যোগ করুন',
        'add_new_patient': 'নতুন রোগী যোগ করুন',
        'select_patient_hint': 'বিস্তারিত এবং রিপোর্ট দেখতে বাম থেকে একটি রোগী নির্বাচন করুন।',
        'name': 'নাম',
        'age': 'বয়স',
        'gender': 'লিঙ্গ',
        'address': 'ঠিকানা',
        'phone': 'ফোন',
        'email': 'ইমেইল',
        'save_patient': 'রোগী সংরক্ষণ করুন',
        'add_report': 'রিপোর্ট যোগ করুন',
        'upload_report': 'রিপোর্ট আপলোড করুন',
        'upload_files_hint': 'আপনি সিএসভি, ডক্স ইত্যাদির মতো ফাইল আপলোড করতে পারেন।',
        'upload_file': 'ফাইল আপলোড করুন',
        'enter_data_manually': 'ডেটা ম্যানুয়ালি প্রবেশ করুন',
        'save_report': 'রিপোর্ট সংরক্ষণ করুন',
        'rr_variance': 'আরআর ইন্টারভাল বৈভব',
        'glucose_age': 'গ্লুকোজ বয়স',
        'meal_timing': 'খাবারের সময়',
        'activity_level': 'কার্যকলাপের স্তর',
        'glucose_range': 'গ্লুকোজ পরিসীমা',
        'breath_depth': 'শ্বাসের গভীরতা',
        'rest_vs_exercise': 'বিশ্রাম বনাম ব্যায়াম',
        'speech_rate': 'কথার হার',
        'pause_frequency': 'বিরাম ফ্রিকোয়েন্সি',
        'pitch_variability': 'পিচ পরিবর্তনশীলতা',
        'text_sentiment': 'পাঠ্য অনুভূতি',
        'voice_emotion': 'ভয়েস আবেগ',
        'facial_emotion': 'মুখের আবেগ',
        'head_tilt': 'মাথার কাত',
        'shoulder_alignment': 'কাঁধের সংযোগ',
        'spine_angle': 'মেরুদণ্ড কোণ',
        'id': 'আইডি',
        'about_para1': 'পুনর্বাসন রোগীদের প্রায়ই ক্রমাগত, বহু-প্যারামিটার পর্যবেক্ষণের প্রয়োজন স্থিতিশীল পুনরুদ্ধার নিশ্চিত করতে এবং জটিলতা প্রাথমিকভাবে সনাক্ত করতে। তবে বেশিরভাগ বিদ্যমান সমাধান শুধুমাত্র হৃদস্পন্দন, মুদ্রা বা গ্লুকোজ স্তরের মতো স্বাস্থ্যের একটি দিক সম্বোধন করে, যার ফলে খণ্ডিত যত্ন হয়।',
        'about_para2': 'RehabSense একটি ইউনিফাইড, বুদ্ধিমান, মাল্টি-মোডাল স্বাস্থ্য পর্যবেক্ষণ প্ল্যাটফর্মের মাধ্যমে এই ব্যবধান পূরণ করার জন্য ডিজাইন করা হয়েছে। এটি প্রধান স্বাস্থ্য সূচকগুলির বিশ্লেষণকে একীভূত করে, যার মধ্যে হৃদস্পন্দনের অনিয়ম, অনুমানিত রক্ত গ্লুকোজ প্রবণতা, শ্বাসপ্রশ্বাসের প্যাটার্ন, বক্তৃতা বৈশিষ্ট্য, আবেগের স্থিতি এবং মুদ্রা রয়েছে একটি সমন্বিত সিস্টেমে।',
        'about_para3': 'RehabSense-এর একটি মূল বৈশিষ্ট্য হল এর রিয়েল-টাইম, ভিডিও-ভিত্তিক মুদ্রা সনাক্তকরণ, যা বিশেষায়িত হার্ডওয়্যারের প্রয়োজন ছাড়াই শরীরের সারিবদ্ধতা এবং আন্দোলনের নির্ভুল ট্র্যাকিং সক্ষম করে।',
        'about_para4': 'প্ল্যাটফর্মটি একটি ব্যবহারকারী-বান্ধব ওয়েব ইন্টারফেসও প্রদান করে যেখানে রোগীরা স্বাস্থ্য ডেটা লগ করতে, ঐতিহাসিক রেকর্ড অ্যাক্সেস করতে এবং স্বজ্ঞাত বিশ্লেষণের মাধ্যমে অগ্রগতি দেখাতে পারেন।',
        'service1_title': 'রিয়েল-টাইম ডায়াগনসিস পান',
        'service1_desc': 'আমাদের উন্নত এআই-চালিত পর্যবেক্ষণ সিস্টেমের মাধ্যমে ইন্টারেক্টিভ চার্ট এবং সম্পূর্ণ অস্বাভাবিকতা সনাক্তকরণ সহ তাৎক্ষণিক স্বাস্থ্য বিশ্লেষণ অনুভব করুন।',
        'service2_title': 'দুর্দান্ত ভিজ্যুয়াল এবং চার্ট',
        'service2_desc': 'স্বজ্ঞাত ভিজ্যুয়ালাইজেশন সহ আপনার স্বাস্থ্য অন্তর্দৃষ্টি সুন্দরভাবে বুঝুন এবং সম্পূর্ণ, সহজ-পাঠযোগ্য চার্টের সাথে আপনার পুনর্বাসন অগ্রগতি ট্র্যাক করুন।',
        'service3_title': 'রিয়েল-টাইম সুপারিশ',
        'service3_desc': 'আপনার নির্দিষ্ট স্বাস্থ্য অবস্থা এবং পুনরুদ্ধার লক্ষ্যের জন্য কাস্টমাইজ করা ব্যক্তিগত ব্যায়াম রুটিন, খাদ্যতালিকাগত নির্দেশনা এবং ডাক্তারের পরামর্শ পান।',
        'service4_title': 'বহুভাষিক সমর্থন',
        'service4_desc': 'আপনার পছন্দের ভাষায় আমাদের প্ল্যাটফর্মে অ্যাক্সেস করুন সম্পূর্ণ বহুভাষিক সমর্থনের সাথে, যা ভাষার বাধা নির্বিশেষে সবার জন্য স্বাস্থ্যসেবা প্রবেশযোগ্য করে তোলে।',
        'our_services': 'আমাদের সেবা',
        'educational_prototype': 'শিক্ষামূলক প্রোটোটাইপ শুধুমাত্র',
        'disclaimer': 'এই সিস্টেম প্রদর্শনের উদ্দেশ্যে এবং চিকিৎসাগত পরামর্শ প্রদান করে না। চিকিৎসাগত সিদ্ধান্তের জন্য সর্বদা যোগ্য স্বাস্থ্যসেবা পেশাদারদের পরামর্শ করুন।',
        'copyright': '© 2026 RehabSense - এআই পুনর্বাসন পর্যবেক্ষণ সিস্টেম',
        'status_normal': 'সাধারণ',
        'status_bradycardia': 'ব্র্যাডিকার্ডিয়া',
        'status_tachycardia': 'ট্যাকিকার্ডিয়া',
        'status_irregular': 'অনিয়মিত',
        'status_low': 'কম',
        'status_high': 'উচ্চ',
        'status_shallow_breathing': 'অগভীর শ্বাস',
        'status_apnea_risk': 'অ্যাপনিয়া ঝুঁকি',
        'status_normal_speech': 'সাধারণ বক্তৃতা',
        'status_slurred_speech': 'অস্পষ্ট/ধীর',
        'status_stressed_speech': 'চাপপূর্ণ বক্তৃতা',
        'status_happy': 'খুশি',
        'status_neutral': 'নিরপেক্ষ',
        'status_stressed': 'চাপপূর্ণ',
        'status_sad': 'দুঃখী',
        'status_good_posture': 'ভাল মুদ্রা',
        'status_forward_head': 'এগিয়ে যাওয়া মাথার মুদ্রা',
        'status_slouched': 'খোঁড়া বসা',
        'bpm': 'bpm',
        'breathing_rate': 'শ্বাসের হার',
        'breaths_per_min': 'শ্বাস/মিনিট',
        'words_per_min': 'শব্দ/মিনিট',
        'out_of_100': '/100',
        'report_title': 'রিপোর্ট',
    },
    'mr': {
        'app_name': 'RehabSense', 'nav_home': 'होम', 'nav_dashboard': 'डॅशबोर्ड', 'nav_progress': 'प्रगती', 'nav_contact': 'संपर्क', 'nav_logout': 'बाहेर विचलित', 'nav_login': 'लॉगिन', 'hero_title': 'RehabSense', 'hero_tagline': 'तुमचा स्मार्ट पुनर्वसन सहाय्यक', 'get_started': 'सुरू करा', 'about_heading': 'RehabSense विषयी', 'login_options': 'लॉगिन पर्याय', 'login_as_patient': 'रुग्ण म्हणून लॉगिन', 'login_as_admin': 'प्रशासक म्हणून लॉगिन', 'patient_id': 'रुग्ण आयडी', 'password': 'पासवर्ड', 'submit': 'लॉगिन', 'invalid_credentials': 'अवैध रुग्ण आयडी किंवा पासवर्ड.', 'welcome': 'स्वागत आहे', 'your_health_reports': 'आपल्या आरोग्य अहवाल', 'view_details': 'तपशील पहा', 'view_progress': 'कालांतराने प्रगती पहा', 'admin_dashboard': 'अॅडमिन डॅशबोर्ड', 'language': 'भाषा', 'about_para1': 'पुनर्वसन रोगীंना स्थिर पुनरुचना सुनिश्चित करण्यासाठी आणि सक्षम अवस्थेत अडचणी शोधण्यासाठी सतत, बहु-पॅरामीटर निरीक्षण आवश्यक असते. तथापि, बहुतेक विद्यमान समाधान केवळ हृदयाचा स्पंद, मुद्रा किंवा ग्लुकोज स्तर यासारख्या आरोग्याच्या एका पहलूला संबोधित करतात, ज्यामुळे खंडित काळजी होते.', 'about_para2': 'RehabSense एकीकृत, बुद्धिमान, बहु-मोडल स्वास्थ्य निरीक्षण प्लॅटफॉर्मद्वारे या अंतराला घेण्यासाठी डिজाइन केले आहे. हे मुख्य आरोग्य सूचकांचे विश्लेषण एकत्रित करते, दिल्याची अनियमितता, अनुमानित रक्त ग्लूकोज ट्रेंड्स, श्वसन नमुने, बोलण्याची वैशिष्ट्ये, भावनिक स्थिती आणि मुद्रा, एक समन्वित प्रणालीमध्ये.', 'about_para3': 'RehabSense चे एक मुख्य वैशिष्ट्य म्हणजे त्याचे रिअल-टाइम, व्हिडिओ-आधारित मुद्रा संपादन, जे विशेष हार्डवेअरचा आवश्यकता न ठेवता शरीर संरेखन आणि हालचालींचे अचूक ट्रॅकिंग सक्षम करते.', 'about_para4': 'प्लॅटफॉर्म एक वापरकर्ता-अनुकूल वेब इंटरफेस देखील प्रदान करतो जेथे रोगी आरोग्य डेटा लॉग करू शकतात, ऐतिहासिक रेकॉर्ड अ‍ॅक्सेस करू शकतात आणि सुज्ञ विश्लेषण द्वारे प्रगती दृश्यमान करू शकतात.', 'service1_title': 'रिअल-टाइम निदान मिळवा', 'service1_desc': 'आमच्या प्रगत एआই-संचालित निरीक्षण प्रणालीद्वारे परस्पर चार्ट आणि व्यापक विसंगती सनावणीसह तात्कालिक आरोग्य विश्लेषण अनुभव करा.', 'service2_title': 'उत्तम दृश्य आणि चार्ट', 'service2_desc': 'अंतर्ज्ञान व्हिजुअलाइজेशनसह आपल्या आरोग्य अंतर्दृष्टी सुंदरपणे समजून घ्या आणि व्यापक, सहज-वाचनीय चार्टसह आपली पुनर्वसन प्रगती ट्रॅक करा.', 'service3_title': 'रिअल-टाइम सुझाव', 'service3_desc': 'आपल्या विशिष्ट आरोग्य परिस्थितीनुसार आणि पुनरुचना लक्ष्यांसाठी व्यक्तिगत व्यायाम दिनचर्या, आहार मार्गदर्शन आणि डॉक्टर सुझाव प्राप्त करा.', 'service4_title': 'बहुभाषिक समर्थन', 'service4_desc': 'आपल्या पसंदीच्या भाषेत आमच्या प्लॅटफॉर्मला व्यापक बहुभाषिक समर्थनसह प्रवेश करा, ज्यामुळे भाषा अडचणीच्या पर्वा न करता सर्वांसाठी स्वास्थ्यसेवा सुलभ होते.', 'our_services': 'आमच्या सेवा', 'educational_prototype': 'शैक्षणिक प्रोटोटाइप केवळ', 'disclaimer': 'ही प्रणाली प्रदर्शन उद्देशांसाठी आहे आणि वैद्यकीय सल्ला प्रदान करत नाही. वैद्यकीय निर्णयांसाठी नेहमी योग्य स्वास्थ्य व्यावसायिकांचा सल्ला घ्या.', 'copyright': '© 2026 RehabSense - एआই पुनर्वसन निरीक्षण प्रणाली', 'status_normal': 'सामान्य', 'status_bradycardia': 'ब्रॅडिकार्डिया', 'status_tachycardia': 'टॅकिकार्डिया', 'status_irregular': 'अनियमित', 'status_low': 'कमी', 'status_high': 'उच्च', 'status_shallow_breathing': 'उथळ श्वास', 'status_apnea_risk': 'अप्निया जोखीम', 'status_normal_speech': 'सामान्य बोलणे', 'status_slurred_speech': 'ढीजड/मंद', 'status_stressed_speech': 'तणावपूर्ण बोलणे', 'status_happy': 'खुश', 'status_neutral': 'तटस्थ', 'status_stressed': 'तणावग्रस्त', 'status_sad': 'दु:खी', 'status_good_posture': 'चांगली मुद्रा', 'status_forward_head': 'पुढे सिरा मुद्रा', 'status_slouched': 'खोडून बसणे'
    },
    'ta': {
        'app_name': 'RehabSense', 'nav_home': 'முகப்பு', 'nav_dashboard': 'டேஷ்போர்டு', 'nav_progress': 'முன்னேற்றம்', 'nav_contact': 'தொடர்பு', 'nav_logout': 'வெளியேறு', 'nav_login': 'உள்நுழைக', 'hero_title': 'RehabSense', 'hero_tagline': 'உங்கள் நுண்ணறிவு மறுவடிவமைப்பு உதவியாளர்', 'get_started': 'தொடங்கு', 'about_heading': 'RehabSense பற்றி', 'login_options': 'உள்நுழைய விருப்பங்கள்', 'login_as_patient': 'நோயாளியாக உள்நுழைய', 'login_as_admin': 'நிர்வாகியாக உள்நுழைய', 'patient_id': 'நோயாளி ஐடி', 'password': 'கடவுச்சொல்', 'submit': 'உள்நுழைய', 'invalid_credentials': 'தவறான நோயாளி ஐடி அல்லது கடவுச்சொல்.', 'welcome': 'வா', 'your_health_reports': 'உங்கள் உடல்நிலை அறிக்கைகள்', 'view_details': 'விவரங்களை காண்க', 'view_progress': 'நேரத்தைக் குறித்து முன்னேற்றம் பாருங்கள்', 'admin_dashboard': 'நிர்வாக டேஷ்போர்டு', 'language': 'மொழி', 'about_para1': 'மறுவடிவமைப்பு நோயாளிகள் பெரும்பாலும் நிலையான மீட்பு உறுதிப்படுத்தவும் சிக்கல்களை முந்தைய கட்டத்தில் கண்டறியவும் தொடர்ச்சியான, பல-அளவுருக்கள் கண்காணிப்பு தேவை. இருப்பினும், பெரும்பாலான বিদ்யமான தீர்வுகள் இதயத்துடிப்பு, தோற்றம் அல்லது குளுக்கோஸ் நிலைகளின் போன்ற ஒரேயொரு ஆரோக்கிய அம்சத்தை நோக்கினால், நொறுங்கிய பராமரிப்பில் விளைகிறது.', 'about_para2': 'RehabSense என்பது ஒரு ஒன்றுபட்ட, புத்திமான், பல-பயன்முறை ஆரோக்கிய கண்காணிப்பு மंच மூலம் இந்த இடைவெளி நிரப்ப ডிজाइन செய்யப்பட்டுள்ளது. இது முக்கிய ஆரோக்கிய சूचకங்களின் பகுப்பாய்வு ஒன்றிணைக்கிறது, இதயத்துடிப்பு முறைகேடு, மதிப்பிடப்பட்ட இரத்த குளுக்கோஸ் போக்குகள், சுவாசக் நடைமுறைகள், பேச்சு பண்புகள், உணர்ச்சி நிலை மற்றும் தோற்றம் ஒரு ஒத்திசைந்த அமைப்புக்குள்.', 'about_para3': 'RehabSense-ன் ஒரு முக்கிய பண்பு அதன் நிஜ-நேர, வீடியோ-அடிப்படை தோற்ற সনாக்தம், இது சிறப்பு வன்பொருளின் தேவை இல்லாமல் உடல் சம்மிதி மற்றும் இயக்கத்தின் துல்லிய பதிவரிப்பை செயல்படுத்துகிறது.', 'about_para4': 'மंच ஒரு பயனர்-நன்றாக வலையூனி இடைமுக வழங்குகிறது அங்கு நோயாளிகள் ஆரோக்கிய தரவு பனிக்கூட, வரலாற்று உபயோகங்கள் அணுக, மற்றும் உருவாசாய்ந்த பகுப்பாய்வு மூலம் முன்னேற்றம் கண்டுபிடிக்க முடியும்.', 'service1_title': 'நிஜ-நேர நির்ணயம் பெறு', 'service1_desc': 'எங்கள் மேம்பட்ட எஐ-செயல்விளைவு கண்காணிப்பு அமைப்பால் ஆட்டம் வரைபுகள் மற்றும் வளை முறைகேடு শোட்டுடன் தত்काலம் ஆரோக்கிய பகுப்பாய்வு சரிபார்க்க.', 'service2_title': 'அருமையான दೃಶ್ಯ மற்றும் வரைபுகள்', 'service2_desc': 'உள்ளுணர்வு दೃಶ್ಯуकरण நன्றாக உங்கள் ஆரோக்கிய அனுसार புரிந்து கொண்டு மற்றும் আইडीक தபசीली, எளிய வாசிக்கிறது வரைபுகளுடன் உங்கள் மறுவடிவமைப்பு தொலைக் என்பதை பிடிக்குங்கள்.', 'service3_title': 'நிஜ-நேர பரிந்துரைகள்', 'service3_desc': 'உங்கள் குறிப்பிட்ட ஆரோக்கிய நிலை மற்றும் பத்தினி உபகারணைக்கு தெரிந்துக்கொள்ளிய ஆற்றलায்ம உபயோகிக்க பயிற்சி, நிவேதனங்கள் மற்றும் பொதுவுரை யோசிக்கப்பட்ட सुझाव प्राप्त करु.', 'service4_title': 'கொலாभाषிক समर्थन', 'service4_desc': 'உங்கள் விரும்பிய भाषेয் приलοгिक्की पलेटфорि युเพาह् समेषटा भाषिक смಹsupport् सही छาপुङ्, भाषा रुकावटिनिर्मात সबkęिभयاਚ್तാᅥ्य आरोक्य सேवा सुलभ दें.', 'our_services': 'எம भоजkि', 'educational_prototype': 'शिक्षामyeli prototaipi পরଶ', 'disclaimer': 'यह सिस्टमॉ प्रदर्शन उদ्देश्यોomaತなीन्दिहీ व्यщை सल्लहनीभी सढბদയां लोगוំՀоटӀभుັ मेಡೀಿნึnáбઓ सḷ్.', 'copyright': '© 2026 RehabSense - एॎ पुन्ರ्वસूన निर्नेयेన рिνĻఫ్رิमീ϶ृौ్ిఢъೆೇੂொীϱ്ीതീ์ตொதംုӗेംుәუоഥీ/', 'status_normal': 'सामೂญဂಠಾಿ', 'status_bradycardia': '브्रדಡিկार्तಿа', 'status_tachycardia': 'टොсಮीಈार್तుीา', 'status_irregular': 'அనียмિत', 'status_low': 'कम', 'status_high': 'უ्тೄถ्ೆ', 'status_shallow_breathing': 'उञ్संಮ्नेśજ्பಾ', 'status_apnea_risk': 'অṟ់ஞ್ఠಿยिउ্ଣిိ', 'status_normal_speech': 'सामञ్ాญ करேช్ఛిՀ೦్ோი', 'status_slurred_speech': 'ढ్ೆᇠ್వईіમ్', 'status_stressed_speech': 'तજ्நொავяြ్ଝాు०್', 'status_happy': 'खுш', 'status_neutral': 'तטस్్్ึັ', 'status_stressed': 'तुщァ్್ಾᄄՀuੇՁุჩ', 'status_sad': 'دುఠ್్ఈு्', 'status_good_posture': 'चींчఎ్్००ՀჯెǑ', 'status_forward_head': 'pाఠु్్ుිูี์್ఠuี្', 'status_slouched': 'خుుีັುూ్००ীืี'
    },
    'kn': {
        'app_name': 'RehabSense', 'nav_home': 'ಮುಖಪುಟ', 'nav_dashboard': 'ಡ್ಯಾಶ್‌ಬೋರ್ಡ್', 'nav_progress': 'ಪ್ರಗತಿ', 'nav_contact': 'ಸಂಪರ್ಕ', 'nav_logout': 'ಲಾಗ್ ಔಟ್', 'nav_login': 'ಲಾಗಿನ್', 'hero_title': 'RehabSense', 'hero_tagline': 'ನಿಮ್ಮ ಸ್ಮಾರ್ಟ್ ಪುನರ್ವಸನ ಸಹಾಯಕ', 'get_started': 'ಆರಂಭಿಸಿ', 'about_heading': 'RehabSense ಬಗ್ಗೆ', 'login_options': 'ಲಾಗಿನ್ ಆಯ್ಕೆಗಳು', 'login_as_patient': 'ರೋಗಿಯಾಗಿಯಾಗಿ ಲಾಗಿನ್ ಮಾಡಿ', 'login_as_admin': 'ನಿರ್ವಹಣೆಗಾರನಾಗಿ ಲಾಗಿನ್ ಮಾಡಿ', 'patient_id': 'ರೋಗಿ ಐಡಿ', 'password': 'ಗೂಪ್ತ ಸೀಟು', 'submit': 'ಲಾಗಿನ್', 'invalid_credentials': 'ಅಮಾನ್ಯ ರೋಗಿ ಐಡಿ ಅಥವಾ ಪರವಾನಗಿ.', 'welcome': 'ಸ್ವಾಗತ', 'your_health_reports': 'ನಿಮ್ಮ ಆರೋಗ್ಯ ವರದಿಗಳು', 'view_details': 'ವಿವರಗಳನ್ನು ನೋಡಿ', 'view_progress': 'ಕಾಲಕಾಲಕ್ಕೆ ಪ್ರಗತಿಯನ್ನು ನೋಡಿ', 'admin_dashboard': 'ಅಡ್ಮಿನ್ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್', 'language': 'ಭಾಷೆ', 'about_para1': 'Rehabilitation patients often need continuous, multi-parameter monitoring to ensure steady recovery and to detect complications at an early stage.', 'about_para2': 'RehabSense is designed to bridge this gap through a unified, intelligent, multi-modal health monitoring platform.', 'about_para3': 'A core feature of RehabSense is its real-time, video-based posture detection.', 'about_para4': 'The platform also provides a user-friendly web interface where patients can log health data, access historical records, and visualize progress.', 'service1_title': 'Real-time Diagnosis', 'service1_desc': 'Experience instant health analysis with interactive charts and comprehensive abnormality detection.', 'service2_title': 'Great Visuals', 'service2_desc': 'Understand your health insights with intuitive visualizations and tracking charts.', 'service3_title': 'Real-time Recommendations', 'service3_desc': 'Receive personalized exercise routines and health suggestions tailored to your condition.', 'service4_title': 'Multilingual Support', 'service4_desc': 'Access in your preferred language for accessible healthcare.', 'our_services': 'Our Services', 'educational_prototype': 'Educational Prototype Only', 'disclaimer': 'This system is for demonstration purposes and does not provide medical advice.', 'copyright': '© 2026 RehabSense', 'status_normal': 'Normal', 'status_bradycardia': 'Bradycardia', 'status_tachycardia': 'Tachycardia', 'status_irregular': 'Irregular', 'status_low': 'Low', 'status_high': 'High', 'status_shallow_breathing': 'Shallow Breathing', 'status_apnea_risk': 'Apnea Risk', 'status_normal_speech': 'Normal Speech', 'status_slurred_speech': 'Slurred/Slow', 'status_stressed_speech': 'Stressed Speech', 'status_happy': 'Happy', 'status_neutral': 'Neutral', 'status_stressed': 'Stressed', 'status_sad': 'Sad', 'status_good_posture': 'Good Posture', 'status_forward_head': 'Forward Head Posture', 'status_slouched': 'Slouched'
    },
    'te': {
        'app_name': 'RehabSense', 'nav_home': 'హోమ్', 'nav_dashboard': 'డాష్‌బోర్డు', 'nav_progress': 'పురోగతి', 'nav_contact': 'సంప్రదించండి', 'nav_logout': 'లాగౌట్', 'nav_login': 'లాగిన్', 'hero_title': 'RehabSense', 'hero_tagline': 'మీ స్మార్ట్ పునరుద్ధరణ సహాయకుడు', 'get_started': 'ప్రారంభించండి', 'about_heading': 'RehabSense గురించి', 'login_options': 'లాగిన్ ఎంపికలు', 'login_as_patient': 'రోగిగా లాగిన్', 'login_as_admin': 'నిర్వాహకుడిగా లాగిన్', 'patient_id': 'రోగి ఐడీ', 'password': 'పాస్వర్డ్', 'submit': 'లాగిన్', 'invalid_credentials': 'చెల్లని రోగి ఐడి లేదా పాస్వర్డ్.', 'welcome': 'స్వాగతం', 'your_health_reports': 'మీ ఆరోగ్య నివేదికలు', 'view_details': 'వివరాలు చూడండి', 'view_progress': 'సమయానుసారం పురోగతిని చూడండి', 'admin_dashboard': 'అడ్మిన్ డ్యాష్‌బోర్డు', 'language': 'భాష', 'about_para1': 'Rehabilitation patients often need continuous, multi-parameter monitoring.', 'about_para2': 'RehabSense is your unified intelligent health monitoring platform.', 'about_para3': 'Real-time video-based posture detection for accurate tracking.', 'about_para4': 'User-friendly web interface for health data and progress tracking.', 'service1_title': 'Real-time Diagnosis', 'service1_desc': 'Instant health analysis with interactive charts.', 'service2_title': 'Great Visuals', 'service2_desc': 'Intuitive visualizations and tracking charts.', 'service3_title': 'Real-time Recommendations', 'service3_desc': 'Personalized health suggestions tailored to your condition.', 'service4_title': 'Multilingual Support', 'service4_desc': 'Access in your preferred language.', 'our_services': 'Our Services', 'educational_prototype': 'Educational Prototype Only', 'disclaimer': 'For demonstration only - consult healthcare professionals.', 'copyright': '© 2026 RehabSense', 'status_normal': 'Normal', 'status_bradycardia': 'Bradycardia', 'status_tachycardia': 'Tachycardia', 'status_irregular': 'Irregular', 'status_low': 'Low', 'status_high': 'High', 'status_shallow_breathing': 'Shallow Breathing', 'status_apnea_risk': 'Apnea Risk', 'status_normal_speech': 'Normal Speech', 'status_slurred_speech': 'Slurred/Slow', 'status_stressed_speech': 'Stressed Speech', 'status_happy': 'Happy', 'status_neutral': 'Neutral', 'status_stressed': 'Stressed', 'status_sad': 'Sad', 'status_good_posture': 'Good Posture', 'status_forward_head': 'Forward Head Posture', 'status_slouched': 'Slouched'
    },
    'or': {
        'app_name': 'RehabSense', 'nav_home': 'ହୋମ୍', 'nav_dashboard': 'ଡ୍ୟାଶବୋର୍ଡ', 'nav_progress': 'ପ୍ରଗତି', 'nav_contact': 'ସମ୍ପର୍କ', 'nav_logout': 'ଲଗ୍ ଆଉଟ୍', 'nav_login': 'ଲଗ୍ଇନ୍', 'hero_title': 'RehabSense', 'hero_tagline': 'ଆପଣଙ୍କର ସ୍ମାର୍ଟ ପୁନଃସଂରଚନା ସହାୟକ', 'get_started': 'ଆରମ୍ଭ କରନ୍ତୁ', 'about_heading': 'RehabSense ବିଷୟରେ', 'login_options': 'ଲଗ୍ଇନ୍ ବିକଳ୍ପ', 'login_as_patient': 'ରୋଗୀ ଭାବେ ଲଗ୍ଇନ୍', 'login_as_admin': 'ନିୟମକ ଭାବେ ଲଗ୍ଇନ୍', 'patient_id': 'ରୋଗୀ ଆଇଡି', 'password': 'ପାସୱାର୍ଡ', 'submit': 'ଲଗ୍ଇନ୍', 'invalid_credentials': 'ଅବୈଧ ରୋଗୀ ଆଇଡି କିମ୍ବା ପାସୱାର୍ଡ.', 'welcome': 'ସ୍ୱାଗତ', 'your_health_reports': 'ଆପଣଙ୍କର ସ୍ୱାସ୍ଥ୍ୟ ରିପୋର୍ଟ', 'view_details': 'ବିବରଣୀ ଦେଖନ୍ତୁ', 'view_progress': 'ସମୟ ସହ ଉନ୍ନତି ଦେଖନ୍ତୁ', 'admin_dashboard': 'ଅଡ୍ମିନ୍ ଡ୍ୟାଶବୋର୍ଡ', 'language': 'ଭାଷା', 'about_para1': 'Continuous patient monitoring system.', 'about_para2': 'Unified health monitoring platform.', 'about_para3': 'Real-time posture detection technology.', 'about_para4': 'User-friendly health tracking interface.', 'service1_title': 'Real-time Diagnosis', 'service1_desc': 'Instant health analysis.', 'service2_title': 'Great Visuals', 'service2_desc': 'Intuitive visualizations.', 'service3_title': 'Real-time Recommendations', 'service3_desc': 'Personalized suggestions.', 'service4_title': 'Multilingual Support', 'service4_desc': 'Multiple language access.', 'our_services': 'Our Services', 'educational_prototype': 'Demonstration Only', 'disclaimer': 'For educational purposes only.', 'copyright': '© 2026 RehabSense', 'status_normal': 'Normal', 'status_bradycardia': 'Bradycardia', 'status_tachycardia': 'Tachycardia', 'status_irregular': 'Irregular', 'status_low': 'Low', 'status_high': 'High', 'status_shallow_breathing': 'Shallow Breathing', 'status_apnea_risk': 'Apnea Risk', 'status_normal_speech': 'Normal Speech', 'status_slurred_speech': 'Slurred/Slow', 'status_stressed_speech': 'Stressed Speech', 'status_happy': 'Happy', 'status_neutral': 'Neutral', 'status_stressed': 'Stressed', 'status_sad': 'Sad', 'status_good_posture': 'Good Posture', 'status_forward_head': 'Forward Head Posture', 'status_slouched': 'Slouched'
    },
    'pa': {
        'app_name': 'RehabSense', 'nav_home': 'ਹੋମ', 'nav_dashboard': 'ਡੈਸ਼ਬੋਰਡ', 'nav_progress': 'ਪ੍ਰਗਤੀ', 'nav_contact': 'ਸੰਪਰਕ', 'nav_logout': 'ਲਾਗ ਆਊਟ', 'nav_login': 'ਲਾਗਿਨ', 'hero_title': 'RehabSense', 'hero_tagline': 'ਤੁਹਾਡਾ ਸਮਾਰਟ ਪੁਨਰਵਾਸ ਸਹਾਇਕ', 'get_started': 'ਸ਼ੁਰੂ ਕਰੋ', 'about_heading': 'RehabSense ਬਾਰੇ', 'login_options': 'ਲਾਗਿਨ ਵਿਕਲਪ', 'login_as_patient': 'ਰੋਗੀ ਵਜੋਂ ਲਾਗਿਨ', 'login_as_admin': 'ਐਡਮਿਨ ਵਜੋਂ ਲਾਗਿਨ', 'patient_id': 'ਰੋਗੀ ਆਈਡੀ', 'password': 'ਪਾਸਵਰਡ', 'submit': 'ਲਾਗਿਨ', 'invalid_credentials': 'ਗਲਤ ਰੋਗੀ ਆਈਡੀ ਜਾਂ ਪਾਸਵਰਡ.', 'welcome': 'ਸਤ ਸ੍ਰੀ ਅਕਾਲ', 'your_health_reports': 'ਤੁਹਾਡੇ ਸਿਹਤ ਰਿਪੋਰਟ', 'view_details': 'ਵੇਰਵੇ ਵੇਖੋ', 'view_progress': 'ਸਮੇਂ ਨਾਲ ਪ੍ਰਗਤੀ ਵੇਖੋ', 'admin_dashboard': 'ਐਡਮਿਨ ਡੈਸ਼ਬੋਰਡ', 'language': 'ਭਾਸ਼ਾ', 'about_para1': 'Continuous patient monitoring system.', 'about_para2': 'Unified health monitoring platform.', 'about_para3': 'Real-time posture detection.', 'about_para4': 'User-friendly health tracking.', 'service1_title': 'Real-time Diagnosis', 'service1_desc': 'Instant health analysis.', 'service2_title': 'Great Visuals', 'service2_desc': 'Intuitive visualizations.', 'service3_title': 'Real-time Recommendations', 'service3_desc': 'Personalized suggestions.', 'service4_title': 'Multilingual Support', 'service4_desc': 'Multiple languages.', 'our_services': 'Our Services', 'educational_prototype': 'Demonstration Only', 'disclaimer': 'Educational use only.', 'copyright': '© 2026 RehabSense', 'status_normal': 'Normal', 'status_bradycardia': 'Bradycardia', 'status_tachycardia': 'Tachycardia', 'status_irregular': 'Irregular', 'status_low': 'Low', 'status_high': 'High', 'status_shallow_breathing': 'Shallow Breathing', 'status_apnea_risk': 'Apnea Risk', 'status_normal_speech': 'Normal Speech', 'status_slurred_speech': 'Slurred/Slow', 'status_stressed_speech': 'Stressed Speech', 'status_happy': 'Happy', 'status_neutral': 'Neutral', 'status_stressed': 'Stressed', 'status_sad': 'Sad', 'status_good_posture': 'Good Posture', 'status_forward_head': 'Forward Head Posture', 'status_slouched': 'Slouched'
    },
    'hry': {
        'app_name': 'RehabSense', 'nav_home': 'होम', 'nav_dashboard': 'डैशबोर्ड', 'nav_progress': 'प्रगति', 'nav_contact': 'संपर्क', 'nav_logout': 'लॉग आउट', 'nav_login': 'लॉग इन', 'hero_title': 'RehabSense', 'hero_tagline': 'तुम्हारा स्मार्ट रीहैब सहायक', 'get_started': 'शुरू कर', 'about_heading': 'RehabSense के बारे में', 'login_options': 'लॉगिन विकल्प', 'login_as_patient': 'मरीज के रूप में लॉगिन', 'login_as_admin': 'एडमिन के रूप में लॉगिन', 'patient_id': 'मरीज आईडी', 'password': 'पासवर्ड', 'submit': 'लॉग इन', 'invalid_credentials': 'गलत मरीज आईडी या पासवर्ड।', 'welcome': 'स्वागत से', 'your_health_reports': 'तेरी हेल्थ रिपोर्ट', 'view_details': 'डिटेल देख', 'view_progress': 'टाइम के साथ प्रगति देख', 'admin_dashboard': 'एडमिन डैशबोर्ड', 'language': 'भाषा', 'about_para1': 'Continuous patient monitoring system.', 'about_para2': 'Unified health monitoring platform.', 'about_para3': 'Real-time posture detection.', 'about_para4': 'User-friendly health tracking.', 'service1_title': 'Real-time Diagnosis', 'service1_desc': 'Instant health analysis.', 'service2_title': 'Great Visuals', 'service2_desc': 'Intuitive visualizations.', 'service3_title': 'Real-time Recommendations', 'service3_desc': 'Personalized suggestions.', 'service4_title': 'Multilingual Support', 'service4_desc': 'Multiple languages.', 'our_services': 'Our Services', 'educational_prototype': 'Demonstration Only', 'disclaimer': 'Educational use only.', 'copyright': '© 2026 RehabSense', 'status_normal': 'Normal', 'status_bradycardia': 'Bradycardia', 'status_tachycardia': 'Tachycardia', 'status_irregular': 'Irregular', 'status_low': 'Low', 'status_high': 'High', 'status_shallow_breathing': 'Shallow Breathing', 'status_apnea_risk': 'Apnea Risk', 'status_normal_speech': 'Normal Speech', 'status_slurred_speech': 'Slurred/Slow', 'status_stressed_speech': 'Stressed Speech', 'status_happy': 'Happy', 'status_neutral': 'Neutral', 'status_stressed': 'Stressed', 'status_sad': 'Sad', 'status_good_posture': 'Good Posture', 'status_forward_head': 'Forward Head Posture', 'status_slouched': 'Slouched'
    },
    'gu': {
        'app_name': 'RehabSense', 'nav_home': 'હોમ', 'nav_dashboard': 'ડેશબોર્ડ', 'nav_progress': 'પ્રગતિ', 'nav_contact': 'સંપર્ક', 'nav_logout': 'લોગ આઉટ', 'nav_login': 'લોગિન', 'hero_title': 'RehabSense', 'hero_tagline': 'તમારો સ્માર્ટ પુનર્વસન સહાયક', 'get_started': 'પ્રારંભ કરો', 'about_heading': 'RehabSense વિશે', 'login_options': 'લોગિન વિકલ્પો', 'login_as_patient': 'રોગી તરીકે લોગિન', 'login_as_admin': 'એડમિન તરીકે લોગિન', 'patient_id': 'રોગી આઈડી', 'password': 'પાસવર્ડ', 'submit': 'લોગિન', 'invalid_credentials': 'અમાન્ય રોગી આઈડી અથવા પાસવર્ડ.', 'welcome': 'સ્વાગત છે', 'your_health_reports': 'તમારી આરોગ્ય રિપોર્ટ્સ', 'view_details': 'વિગતો જુઓ', 'view_progress': 'સમય સાથે પ્રગતિ જુઓ', 'admin_dashboard': 'એડમિન ડેશબોર્ડ', 'language': 'ભાષા', 'about_para1': 'Continuous patient monitoring system.', 'about_para2': 'Unified health monitoring platform.', 'about_para3': 'Real-time posture detection.', 'about_para4': 'User-friendly health tracking.', 'service1_title': 'Real-time Diagnosis', 'service1_desc': 'Instant health analysis.', 'service2_title': 'Great Visuals', 'service2_desc': 'Intuitive visualizations.', 'service3_title': 'Real-time Recommendations', 'service3_desc': 'Personalized suggestions.', 'service4_title': 'Multilingual Support', 'service4_desc': 'Multiple languages.', 'our_services': 'Our Services', 'educational_prototype': 'Demonstration Only', 'disclaimer': 'Educational use only.', 'copyright': '© 2026 RehabSense', 'status_normal': 'Normal', 'status_bradycardia': 'Bradycardia', 'status_tachycardia': 'Tachycardia', 'status_irregular': 'Irregular', 'status_low': 'Low', 'status_high': 'High', 'status_shallow_breathing': 'Shallow Breathing', 'status_apnea_risk': 'Apnea Risk', 'status_normal_speech': 'Normal Speech', 'status_slurred_speech': 'Slurred/Slow', 'status_stressed_speech': 'Stressed Speech', 'status_happy': 'Happy', 'status_neutral': 'Neutral', 'status_stressed': 'Stressed', 'status_sad': 'Sad', 'status_good_posture': 'Good Posture', 'status_forward_head': 'Forward Head Posture', 'status_slouched': 'Slouched'
    },
    'bho': {
        'app_name': 'RehabSense', 'nav_home': 'होम', 'nav_dashboard': 'डैशबोर्ड', 'nav_progress': 'प्रगति', 'nav_contact': 'संपर्क', 'nav_logout': 'लॉग आउट', 'nav_login': 'लॉगिन', 'hero_title': 'RehabSense', 'hero_tagline': 'तोहार स्मार्ट पुनरावास सहायक', 'get_started': 'शुरू कर', 'about_heading': 'RehabSense के बारे में', 'login_options': 'लॉगिन विकल्प', 'login_as_patient': 'मरीज के रूप में लॉगिन', 'login_as_admin': 'एडमिन के रूप में लॉगिन', 'patient_id': 'मरीज आईडी', 'password': 'पासवर्ड', 'submit': 'लॉगिन', 'invalid_credentials': 'गलत मरीज आईडी या पासवर्ड।', 'welcome': 'स्वागत बा', 'your_health_reports': 'तोहार स्वास्थ्य रिपोर्ट', 'view_details': 'विवरण देखें', 'view_progress': 'समय के साथ प्रगति देखें', 'admin_dashboard': 'एडमिन डैशबोर्ड', 'language': 'भाषा'
    },
    'ur': {
        'app_name': 'RehabSense', 'nav_home': 'ہوم', 'nav_dashboard': 'ڈیش بورڈ', 'nav_progress': 'پیش رفت', 'nav_contact': 'رابطہ', 'nav_logout': 'لاگ آؤٹ', 'nav_login': 'لاگ ان', 'hero_title': 'RehabSense', 'hero_tagline': 'آپ کا اسمارٹ ریہیب معاون', 'get_started': 'شروع کریں', 'about_heading': 'RehabSense کے بارے میں', 'login_options': 'لاگ ان کے اختیارات', 'login_as_patient': 'مریض کے طور پر لاگ ان کریں', 'login_as_admin': 'ایڈمن کے طور پر لاگ ان کریں', 'patient_id': 'مریض شناخت', 'password': 'پاس ورڈ', 'submit': 'لاگ ان', 'invalid_credentials': 'غلط مریض شناخت یا پاس ورڈ۔', 'welcome': 'خوش آمدید', 'your_health_reports': 'آپ کی صحت کی رپورٹس', 'view_details': 'تفصیلات دیکھیں', 'view_progress': 'وقت کے ساتھ پیش رفت دیکھیں', 'admin_dashboard': 'ایڈمن ڈیش بورڈ', 'language': 'زبان', 'about_para1': 'Continuous patient monitoring system.', 'about_para2': 'Unified health monitoring platform.', 'about_para3': 'Real-time posture detection.', 'about_para4': 'User-friendly health tracking.', 'service1_title': 'Real-time Diagnosis', 'service1_desc': 'Instant health analysis.', 'service2_title': 'Great Visuals', 'service2_desc': 'Intuitive visualizations.', 'service3_title': 'Real-time Recommendations', 'service3_desc': 'Personalized suggestions.', 'service4_title': 'Multilingual Support', 'service4_desc': 'Multiple languages.', 'our_services': 'Our Services', 'educational_prototype': 'Demonstration Only', 'disclaimer': 'Educational use only.', 'copyright': '© 2026 RehabSense', 'status_normal': 'Normal', 'status_bradycardia': 'Bradycardia', 'status_tachycardia': 'Tachycardia', 'status_irregular': 'Irregular', 'status_low': 'Low', 'status_high': 'High', 'status_shallow_breathing': 'Shallow Breathing', 'status_apnea_risk': 'Apnea Risk', 'status_normal_speech': 'Normal Speech', 'status_slurred_speech': 'Slurred/Slow', 'status_stressed_speech': 'Stressed Speech', 'status_happy': 'Happy', 'status_neutral': 'Neutral', 'status_stressed': 'Stressed', 'status_sad': 'Sad', 'status_good_posture': 'Good Posture', 'status_forward_head': 'Forward Head Posture', 'status_slouched': 'Slouched'
    }
}

# Fill missing translation keys from English for all configured languages.
for lang_code in SUPPORTED_LANGUAGES:
    if lang_code not in TRANSLATIONS:
        TRANSLATIONS[lang_code] = TRANSLATIONS['en'].copy()
        continue
    for key, value in TRANSLATIONS['en'].items():
        TRANSLATIONS[lang_code].setdefault(key, value)

# Native UI completion for high-priority languages.
TRANSLATIONS['es'].update({
    'activity_level': 'Nivel de actividad',
    'add_new_patient': 'Agregar nuevo paciente',
    'add_patient': 'Agregar paciente',
    'add_report': 'Agregar informe',
    'address': 'Dirección',
    'admin_id': 'ID de administrador',
    'admin_login': 'Inicio de sesión de administrador',
    'age': 'Edad',
    'ai_analysis': 'Análisis de IA',
    'ai_analysis_results': 'Resultados del análisis de IA',
    'ai_powered_rehab_system': 'Sistema de monitoreo de rehabilitación impulsado por IA',
    'blood_glucose': 'Glucosa en sangre',
    'bmi': 'IMC',
    'breath_depth': 'Profundidad de respiración',
    'breathing_pattern': 'Patrón de respiración',
    'breathing_pattern_status': 'Estado del patrón de respiración',
    'breathing_rate': 'Frecuencia respiratoria',
    'confidence': 'Confianza',
    'data_collection': 'Recolección de datos',
    'drop_mail': 'Enviar correo',
    'email': 'Correo electrónico',
    'emotional_state': 'Estado emocional',
    'emotional_state_distribution': 'Distribución del estado emocional',
    'enter_admin_id': 'Ingresa ID de administrador',
    'enter_data_manually': 'Ingresar datos manualmente',
    'enter_password': 'Ingresa contraseña',
    'enter_patient_id': 'Ingresa ID de paciente',
    'facial_emotion': 'Emoción facial',
    'gender': 'Género',
    'glucose_age': 'Edad (glucosa)',
    'glucose_range': 'Rango de glucosa',
    'head_tilt': 'Inclinación de cabeza',
    'health_metrics_over_time': 'Métricas de salud a lo largo del tiempo',
    'health_status_predictions': 'Predicciones del estado de salud',
    'heart_rate': 'Frecuencia cardíaca',
    'heart_rate_trend': 'Tendencia de frecuencia cardíaca',
    'heartbeat_abnormality_detector': 'Detector de anormalidades del latido',
    'heartbeat_analysis': 'Análisis de latidos',
    'id': 'ID',
    'insights_generation': 'Generación de insights',
    'loading_progress_data': 'Cargando tus datos de progreso...',
    'meal_timing': 'Horario de comidas',
    'name': 'Nombre',
    'patient_login': 'Inicio de sesión de paciente',
    'patient_metrics_collected': 'Las métricas de salud del paciente se recopilan mediante informes',
    'patients': 'Pacientes',
    'pause_frequency': 'Frecuencia de pausas',
    'personalized_exercise_tips': 'Se proporcionan ejercicios y consejos de estilo de vida personalizados',
    'personalized_recommendations': 'Recomendaciones personalizadas',
    'phone': 'Teléfono',
    'pitch_variability': 'Variabilidad del tono',
    'posture_analysis': 'Análisis de postura',
    'posture_score': 'Puntuación de postura',
    'posture_score_progression': 'Progresión de la puntuación de postura',
    'project_overview': 'Resumen del proyecto',
    'rate': 'Tasa',
    'recommendations_heading': 'Recomendaciones',
    'report_title': 'Informe',
    'rest_vs_exercise': 'Reposo vs ejercicio',
    'ring_us': 'Llámanos',
    'rr_variance': 'Varianza del intervalo RR',
    'save_patient': 'Guardar paciente',
    'save_report': 'Guardar informe',
    'select_patient_hint': 'Selecciona un paciente a la izquierda para ver detalles e informes.',
    'sentiment_score': 'Puntuación de sentimiento',
    'services': 'Servicios',
    'shoulder_alignment': 'Alineación de hombros',
    'six_ai_models': 'Seis modelos de IA',
    'six_models_analyze': 'Seis modelos de aprendizaje automático analizan los datos',
    'speech_pattern': 'Patrón de habla',
    'speech_rate': 'Velocidad del habla',
    'spine_angle': 'Ángulo de columna',
    'summary_heading': 'Resumen general',
    'text_sentiment': 'Sentimiento de texto',
    'total_reports': 'Total de informes',
    'tracking_period': 'Período de seguimiento',
    'upload_file': 'Subir archivo',
    'upload_files_hint': 'Puedes subir archivos como CSV, DOCX, etc.',
    'upload_report': 'Subir informe',
    'voice_emotion': 'Emoción de voz',
    'weeks': 'semanas',
    'welcome_admin': 'Bienvenido administrador'
})

TRANSLATIONS['hi'].update({
    'activity_level': 'गतिविधि स्तर',
    'add_new_patient': 'नया मरीज जोड़ें',
    'add_patient': 'मरीज जोड़ें',
    'add_report': 'रिपोर्ट जोड़ें',
    'address': 'पता',
    'admin_id': 'एडमिन आईडी',
    'admin_login': 'एडमिन लॉगिन',
    'age': 'आयु',
    'ai_analysis': 'एआई विश्लेषण',
    'ai_powered_rehab_system': 'एआई-संचालित पुनर्वास मॉनिटरिंग सिस्टम',
    'breath_depth': 'सांस की गहराई',
    'breathing_pattern_status': 'श्वसन पैटर्न स्थिति',
    'breathing_rate': 'श्वसन दर',
    'data_collection': 'डेटा संग्रह',
    'drop_mail': 'ईमेल करें',
    'email': 'ईमेल',
    'emotional_state_distribution': 'भावनात्मक स्थिति वितरण',
    'enter_admin_id': 'एडमिन आईडी दर्ज करें',
    'enter_data_manually': 'डेटा मैन्युअली दर्ज करें',
    'enter_password': 'पासवर्ड दर्ज करें',
    'enter_patient_id': 'रोगी आईडी दर्ज करें',
    'facial_emotion': 'चेहरे की भावना',
    'gender': 'लिंग',
    'glucose_age': 'ग्लूकोज आयु',
    'glucose_range': 'ग्लूकोज रेंज',
    'head_tilt': 'सिर झुकाव',
    'health_metrics_over_time': 'समय के साथ स्वास्थ्य मेट्रिक्स',
    'health_status_predictions': 'स्वास्थ्य स्थिति पूर्वानुमान',
    'heart_rate_trend': 'हृदय गति रुझान',
    'heartbeat_abnormality_detector': 'हृदय धड़कन असामान्यता डिटेक्टर',
    'id': 'आईडी',
    'insights_generation': 'अंतर्दृष्टि निर्माण',
    'loading_progress_data': 'आपका प्रगति डेटा लोड हो रहा है...',
    'meal_timing': 'भोजन समय',
    'name': 'नाम',
    'patient_login': 'रोगी लॉगिन',
    'patient_metrics_collected': 'रोगी स्वास्थ्य मेट्रिक्स रिपोर्टों से एकत्र किए जाते हैं',
    'patients': 'मरीज',
    'pause_frequency': 'रुकावट आवृत्ति',
    'personalized_exercise_tips': 'व्यक्तिगत व्यायाम और जीवनशैली सुझाव दिए जाते हैं',
    'phone': 'फोन',
    'pitch_variability': 'पिच परिवर्तनशीलता',
    'posture_score_progression': 'मुद्रा स्कोर प्रगति',
    'project_overview': 'प्रोजेक्ट अवलोकन',
    'recommendations_heading': 'सिफारिशें',
    'report_title': 'रिपोर्ट',
    'rest_vs_exercise': 'आराम बनाम व्यायाम',
    'ring_us': 'कॉल करें',
    'rr_variance': 'आरआर इंटरवल वैरिएंस',
    'save_patient': 'मरीज सहेजें',
    'save_report': 'रिपोर्ट सहेजें',
    'select_patient_hint': 'विवरण और रिपोर्ट देखने के लिए बाईं ओर से मरीज चुनें।',
    'services': 'सेवाएं',
    'shoulder_alignment': 'कंधे संरेखण',
    'six_ai_models': 'छह एआई मॉडल',
    'six_models_analyze': 'छह प्रशिक्षित मशीन लर्निंग मॉडल डेटा का विश्लेषण करते हैं',
    'speech_rate': 'बोलने की दर',
    'spine_angle': 'रीढ़ का कोण',
    'text_sentiment': 'पाठ भावना',
    'total_reports': 'कुल रिपोर्ट',
    'tracking_period': 'ट्रैकिंग अवधि',
    'upload_file': 'फ़ाइल अपलोड करें',
    'upload_files_hint': 'आप CSV, DOCX आदि फ़ाइलें अपलोड कर सकते हैं।',
    'upload_report': 'रिपोर्ट अपलोड करें',
    'voice_emotion': 'आवाज़ भावना',
    'weeks': 'सप्ताह',
    'welcome_admin': 'एडमिन का स्वागत है'
})

# About page complete i18n keys (English source text; other languages fallback if missing).
TRANSLATIONS['en'].update({
    'about_overview_para': 'RehabSense is an educational prototype demonstrating how artificial intelligence can support rehabilitation patients through comprehensive health monitoring. This system integrates six specialized AI models to analyze different aspects of patient health and provide personalized rehabilitation recommendations.',
    'label_algorithm': 'Algorithm',
    'label_input': 'Input',
    'label_output': 'Output',
    'algo_random_forest_classifier': 'Random Forest Classifier',
    'algo_gradient_boosting_classifier': 'Gradient Boosting Classifier',
    'algo_svm': 'Support Vector Machine (SVM)',
    'algo_logistic_regression': 'Logistic Regression',
    'algo_knn': 'K-Nearest Neighbors (KNN)',
    'algo_decision_tree_classifier': 'Decision Tree Classifier',
    'blood_glucose_estimation': 'Blood Glucose Estimation',
    'breathing_irregularity_detection': 'Breathing Irregularity Detection',
    'speech_pattern_analysis': 'Speech Pattern Analysis',
    'emotional_state_detection': 'Emotional State Detection',
    'real_time_posture_detection': 'Real-Time Posture Detection',
    'heartbeat_model_input': 'Heart rate, RR interval variance',
    'heartbeat_model_output': 'Normal, Bradycardia, Tachycardia, Irregular',
    'glucose_model_input': 'Age, BMI, meal timing, activity level',
    'glucose_model_output': 'Low, Normal, High glucose range',
    'breathing_model_input': 'Breathing rate, breath depth, rest vs exercise',
    'breathing_model_output': 'Normal, Shallow, Irregular, Apnea risk',
    'speech_model_input': 'Speech rate, pause frequency, pitch variability',
    'speech_model_output': 'Normal, Slurred/Slow, Stressed speech',
    'emotion_model_input': 'Text sentiment, voice emotion, facial emotion',
    'emotion_model_output': 'Happy, Neutral, Stressed, Sad',
    'posture_model_input': 'Head tilt, shoulder alignment, spine angle',
    'posture_model_output': 'Good posture, Forward head, Slouched + Score (0-100)',
    'how_it_works': 'How It Works',
    'features_heading': 'Features',
    'feature_1': 'Comprehensive health monitoring across six vital areas',
    'feature_2': 'Real-time AI-powered predictions and analysis',
    'feature_3': 'Personalized rehabilitation recommendations',
    'feature_4': 'Progress tracking over time with visual charts',
    'feature_5': 'Clear, accessible, non-medical language',
    'feature_6': 'Patient-centered design for dignity and inclusivity',
    'educational_purpose_heading': 'Educational Purpose',
    'important_notice': 'Important Notice',
    'educational_notice_strong': 'This is an educational prototype designed to demonstrate AI/ML concepts in healthcare.',
    'educational_point_1': 'Not intended for actual medical diagnosis or treatment',
    'educational_point_2': 'Uses synthetic data for demonstration purposes',
    'educational_point_3': 'Models are simplified for educational clarity',
    'educational_point_4': 'Always consult qualified healthcare professionals for medical advice',
    'future_extensions_heading': 'Future Extensions',
    'future_1': 'Integration with wearable devices (smartwatches, fitness trackers)',
    'future_2': 'Real-time sensor data processing',
    'future_3': 'Multi-language support for global accessibility',
    'future_4': 'Mobile application for on-the-go monitoring',
    'future_5': 'Advanced deep learning models for improved accuracy',
    'future_6': 'Telemedicine integration for remote consultations',
    'future_7': 'Voice-activated interface for accessibility',
    'technology_stack_heading': 'Technology Stack',
    'tech_backend': 'Backend',
    'tech_frontend': 'Frontend',
    'tech_visualization': 'Visualization',
    'tech_storage': 'Storage',
    'tech_storage_value': 'Local file system (JSON)'
})

# Native about-page completion for Spanish.
TRANSLATIONS['es'].update({
    'about_overview_para': 'RehabSense es un prototipo educativo que demuestra cómo la inteligencia artificial puede apoyar a pacientes de rehabilitación mediante monitoreo integral de la salud. Este sistema integra seis modelos de IA especializados para analizar diferentes aspectos de la salud del paciente y ofrecer recomendaciones personalizadas de rehabilitación.',
    'label_algorithm': 'Algoritmo',
    'label_input': 'Entrada',
    'label_output': 'Salida',
    'algo_random_forest_classifier': 'Clasificador Random Forest',
    'algo_gradient_boosting_classifier': 'Clasificador Gradient Boosting',
    'algo_svm': 'Máquina de Vectores de Soporte (SVM)',
    'algo_logistic_regression': 'Regresión Logística',
    'algo_knn': 'K-Vecinos más cercanos (KNN)',
    'algo_decision_tree_classifier': 'Clasificador de Árbol de Decisión',
    'blood_glucose_estimation': 'Estimación de glucosa en sangre',
    'breathing_irregularity_detection': 'Detección de irregularidad respiratoria',
    'speech_pattern_analysis': 'Análisis de patrón del habla',
    'emotional_state_detection': 'Detección del estado emocional',
    'real_time_posture_detection': 'Detección de postura en tiempo real',
    'heartbeat_model_input': 'Frecuencia cardíaca, varianza del intervalo RR',
    'heartbeat_model_output': 'Normal, bradicardia, taquicardia, irregular',
    'glucose_model_input': 'Edad, IMC, horario de comidas, nivel de actividad',
    'glucose_model_output': 'Rango de glucosa bajo, normal, alto',
    'breathing_model_input': 'Frecuencia respiratoria, profundidad de respiración, reposo vs ejercicio',
    'breathing_model_output': 'Normal, superficial, irregular, riesgo de apnea',
    'speech_model_input': 'Velocidad del habla, frecuencia de pausas, variabilidad del tono',
    'speech_model_output': 'Normal, arrastrado/lento, habla estresada',
    'emotion_model_input': 'Sentimiento de texto, emoción de voz, emoción facial',
    'emotion_model_output': 'Feliz, neutral, estresado, triste',
    'posture_model_input': 'Inclinación de cabeza, alineación de hombros, ángulo de columna',
    'posture_model_output': 'Buena postura, cabeza adelantada, encorvado + puntuación (0-100)',
    'how_it_works': 'Cómo funciona',
    'features_heading': 'Características',
    'feature_1': 'Monitoreo integral de salud en seis áreas vitales',
    'feature_2': 'Predicciones y análisis en tiempo real impulsados por IA',
    'feature_3': 'Recomendaciones de rehabilitación personalizadas',
    'feature_4': 'Seguimiento del progreso en el tiempo con gráficos visuales',
    'feature_5': 'Lenguaje claro, accesible y no médico',
    'feature_6': 'Diseño centrado en el paciente para dignidad e inclusión',
    'educational_purpose_heading': 'Propósito educativo',
    'important_notice': 'Aviso importante',
    'educational_notice_strong': 'Este es un prototipo educativo diseñado para demostrar conceptos de IA/ML en salud.',
    'educational_point_1': 'No está destinado para diagnóstico o tratamiento médico real',
    'educational_point_2': 'Usa datos sintéticos con fines de demostración',
    'educational_point_3': 'Los modelos están simplificados para mayor claridad educativa',
    'educational_point_4': 'Consulta siempre a profesionales de salud calificados para consejo médico',
    'future_extensions_heading': 'Extensiones futuras',
    'future_1': 'Integración con dispositivos wearables (relojes inteligentes, rastreadores de actividad)',
    'future_2': 'Procesamiento de datos de sensores en tiempo real',
    'future_3': 'Soporte multilingüe para accesibilidad global',
    'future_4': 'Aplicación móvil para monitoreo en movimiento',
    'future_5': 'Modelos avanzados de aprendizaje profundo para mayor precisión',
    'future_6': 'Integración de telemedicina para consultas remotas',
    'future_7': 'Interfaz activada por voz para accesibilidad',
    'technology_stack_heading': 'Pila tecnológica',
    'tech_backend': 'Backend',
    'tech_frontend': 'Frontend',
    'tech_visualization': 'Visualización',
    'tech_storage': 'Almacenamiento',
    'tech_storage_value': 'Sistema de archivos local (JSON)'
})

# Native about-page completion for Hindi.
TRANSLATIONS['hi'].update({
    'about_overview_para': 'RehabSense एक शैक्षणिक प्रोटोटाइप है जो दिखाता है कि कृत्रिम बुद्धिमत्ता व्यापक स्वास्थ्य निगरानी के माध्यम से पुनर्वास रोगियों की कैसे मदद कर सकती है। यह सिस्टम रोगी स्वास्थ्य के विभिन्न पहलुओं का विश्लेषण करने और व्यक्तिगत पुनर्वास सिफारिशें देने के लिए छह विशेष एआई मॉडलों को एकीकृत करता है।',
    'label_algorithm': 'एल्गोरिदम',
    'label_input': 'इनपुट',
    'label_output': 'आउटपुट',
    'algo_random_forest_classifier': 'रैंडम फॉरेस्ट क्लासिफायर',
    'algo_gradient_boosting_classifier': 'ग्रेडिएंट बूस्टिंग क्लासिफायर',
    'algo_svm': 'सपोर्ट वेक्टर मशीन (SVM)',
    'algo_logistic_regression': 'लॉजिस्टिक रिग्रेशन',
    'algo_knn': 'के-नज़दीकी पड़ोसी (KNN)',
    'algo_decision_tree_classifier': 'डिसीजन ट्री क्लासिफायर',
    'blood_glucose_estimation': 'रक्त शर्करा अनुमान',
    'breathing_irregularity_detection': 'श्वसन अनियमितता पहचान',
    'speech_pattern_analysis': 'भाषण पैटर्न विश्लेषण',
    'emotional_state_detection': 'भावनात्मक स्थिति पहचान',
    'real_time_posture_detection': 'रीयल-टाइम मुद्रा पहचान',
    'heartbeat_model_input': 'हृदय गति, RR इंटरवल वैरिएंस',
    'heartbeat_model_output': 'सामान्य, धीमी हृदय गति, तेज हृदय गति, अनियमित',
    'glucose_model_input': 'आयु, बीएमआई, भोजन समय, गतिविधि स्तर',
    'glucose_model_output': 'निम्न, सामान्य, उच्च ग्लूकोज रेंज',
    'breathing_model_input': 'श्वसन दर, सांस की गहराई, आराम बनाम व्यायाम',
    'breathing_model_output': 'सामान्य, उथली, अनियमित, एपनिया जोखिम',
    'speech_model_input': 'बोलने की दर, रुकावट आवृत्ति, पिच परिवर्तनशीलता',
    'speech_model_output': 'सामान्य, लड़खड़ाता/धीमा, तनावपूर्ण भाषण',
    'emotion_model_input': 'पाठ भावना, आवाज़ भावना, चेहरे की भावना',
    'emotion_model_output': 'खुश, तटस्थ, तनावग्रस्त, उदास',
    'posture_model_input': 'सिर झुकाव, कंधे संरेखण, रीढ़ कोण',
    'posture_model_output': 'अच्छी मुद्रा, आगे की ओर सिर, झुकी हुई मुद्रा + स्कोर (0-100)',
    'how_it_works': 'यह कैसे काम करता है',
    'features_heading': 'विशेषताएं',
    'feature_1': 'छह महत्वपूर्ण क्षेत्रों में व्यापक स्वास्थ्य निगरानी',
    'feature_2': 'रीयल-टाइम एआई-संचालित पूर्वानुमान और विश्लेषण',
    'feature_3': 'व्यक्तिगत पुनर्वास सिफारिशें',
    'feature_4': 'दृश्य चार्ट के साथ समय के साथ प्रगति ट्रैकिंग',
    'feature_5': 'स्पष्ट, सुलभ, गैर-चिकित्सीय भाषा',
    'feature_6': 'गरिमा और समावेशन के लिए रोगी-केंद्रित डिजाइन',
    'educational_purpose_heading': 'शैक्षणिक उद्देश्य',
    'important_notice': 'महत्वपूर्ण सूचना',
    'educational_notice_strong': 'यह एक शैक्षणिक प्रोटोटाइप है जो स्वास्थ्य सेवा में AI/ML अवधारणाओं को प्रदर्शित करने के लिए बनाया गया है।',
    'educational_point_1': 'वास्तविक चिकित्सा निदान या उपचार के लिए नहीं',
    'educational_point_2': 'प्रदर्शन हेतु सिंथेटिक डेटा का उपयोग',
    'educational_point_3': 'शैक्षणिक स्पष्टता के लिए मॉडल सरल बनाए गए हैं',
    'educational_point_4': 'चिकित्सकीय सलाह के लिए हमेशा योग्य स्वास्थ्य विशेषज्ञों से परामर्श करें',
    'future_extensions_heading': 'भविष्य विस्तार',
    'future_1': 'वेयरेबल डिवाइस एकीकरण (स्मार्टवॉच, फिटनेस ट्रैकर)',
    'future_2': 'रीयल-टाइम सेंसर डेटा प्रोसेसिंग',
    'future_3': 'वैश्विक पहुंच के लिए बहुभाषी समर्थन',
    'future_4': 'चलते-फिरते निगरानी के लिए मोबाइल ऐप',
    'future_5': 'बेहतर सटीकता के लिए उन्नत डीप लर्निंग मॉडल',
    'future_6': 'रिमोट परामर्श के लिए टेलीमेडिसिन एकीकरण',
    'future_7': 'सुगम्यता के लिए वॉइस-सक्रिय इंटरफ़ेस',
    'technology_stack_heading': 'तकनीकी स्टैक',
    'tech_backend': 'बैकएंड',
    'tech_frontend': 'फ्रंटएंड',
    'tech_visualization': 'विज़ुअलाइज़ेशन',
    'tech_storage': 'स्टोरेज',
    'tech_storage_value': 'लोकल फ़ाइल सिस्टम (JSON)'
})

# Native about-page completion for Bengali.
TRANSLATIONS['bn'].update({
    'about_overview_para': 'RehabSense একটি শিক্ষামূলক প্রোটোটাইপ যা দেখায় কিভাবে কৃত্রিম বুদ্ধিমত্তা সমন্বিত স্বাস্থ্য পর্যবেক্ষণের মাধ্যমে পুনর্বাসন রোগীদের সহায়তা করতে পারে। এই সিস্টেমটি রোগীর স্বাস্থ্যের বিভিন্ন দিক বিশ্লেষণ করতে এবং ব্যক্তিগতকৃত পুনর্বাসন পরামর্শ দিতে ছয়টি বিশেষায়িত এআই মডেল একীভূত করে।',
    'label_algorithm': 'অ্যালগরিদম',
    'label_input': 'ইনপুট',
    'label_output': 'আউটপুট',
    'algo_random_forest_classifier': 'র‍্যান্ডম ফরেস্ট ক্লাসিফায়ার',
    'algo_gradient_boosting_classifier': 'গ্রেডিয়েন্ট বুস্টিং ক্লাসিফায়ার',
    'algo_svm': 'সাপোর্ট ভেক্টর মেশিন (SVM)',
    'algo_logistic_regression': 'লজিস্টিক রিগ্রেশন',
    'algo_knn': 'কে-নিয়ারেস্ট নেইবার্স (KNN)',
    'algo_decision_tree_classifier': 'ডিসিশন ট্রি ক্লাসিফায়ার',
    'blood_glucose_estimation': 'রক্তে গ্লুকোজের আনুমানিক নির্ধারণ',
    'breathing_irregularity_detection': 'শ্বাস-প্রশ্বাসের অনিয়ম সনাক্তকরণ',
    'speech_pattern_analysis': 'কথার ধরন বিশ্লেষণ',
    'emotional_state_detection': 'আবেগগত অবস্থা সনাক্তকরণ',
    'real_time_posture_detection': 'রিয়েল-টাইম ভঙ্গি সনাক্তকরণ',
    'heartbeat_model_input': 'হৃদস্পন্দনের হার, RR ইন্টারভ্যাল ভ্যারিয়েন্স',
    'heartbeat_model_output': 'স্বাভাবিক, ব্র্যাডিকার্ডিয়া, ট্যাকিকার্ডিয়া, অনিয়মিত',
    'glucose_model_input': 'বয়স, BMI, খাবারের সময়, কার্যকলাপের স্তর',
    'glucose_model_output': 'নিম্ন, স্বাভাবিক, উচ্চ গ্লুকোজ পরিসর',
    'breathing_model_input': 'শ্বাসের হার, শ্বাসের গভীরতা, বিশ্রাম বনাম ব্যায়াম',
    'breathing_model_output': 'স্বাভাবিক, অগভীর, অনিয়মিত, অ্যাপনিয়া ঝুঁকি',
    'speech_model_input': 'কথার গতি, বিরতির ঘনত্ব, পিচের পরিবর্তনশীলতা',
    'speech_model_output': 'স্বাভাবিক, অস্পষ্ট/ধীর, চাপযুক্ত কথা',
    'emotion_model_input': 'টেক্সট সেন্টিমেন্ট, কণ্ঠের আবেগ, মুখের আবেগ',
    'emotion_model_output': 'খুশি, নিরপেক্ষ, চাপযুক্ত, দুঃখী',
    'posture_model_input': 'মাথার ঝোঁক, কাঁধের সমতা, মেরুদণ্ডের কোণ',
    'posture_model_output': 'ভাল ভঙ্গি, সামনে ঝুঁকে থাকা মাথা, কুঁজো + স্কোর (0-100)',
    'how_it_works': 'এটি কীভাবে কাজ করে',
    'features_heading': 'বৈশিষ্ট্যসমূহ',
    'feature_1': 'ছয়টি গুরুত্বপূর্ণ ক্ষেত্রে সমন্বিত স্বাস্থ্য পর্যবেক্ষণ',
    'feature_2': 'রিয়েল-টাইম এআই-চালিত পূর্বাভাস ও বিশ্লেষণ',
    'feature_3': 'ব্যক্তিগতকৃত পুনর্বাসন পরামর্শ',
    'feature_4': 'চিত্রভিত্তিক চার্ট দিয়ে সময়ের সাথে অগ্রগতি ট্র্যাকিং',
    'feature_5': 'পরিষ্কার, সহজলভ্য, অ-চিকিৎসাবিদ্যাগত ভাষা',
    'feature_6': 'মর্যাদা ও অন্তর্ভুক্তির জন্য রোগী-কেন্দ্রিক নকশা',
    'educational_purpose_heading': 'শিক্ষামূলক উদ্দেশ্য',
    'important_notice': 'গুরুত্বপূর্ণ নোটিশ',
    'educational_notice_strong': 'এটি একটি শিক্ষামূলক প্রোটোটাইপ, যা স্বাস্থ্যসেবায় AI/ML ধারণা প্রদর্শনের জন্য তৈরি করা হয়েছে।',
    'educational_point_1': 'বাস্তব চিকিৎসা নির্ণয় বা চিকিৎসার জন্য নয়',
    'educational_point_2': 'প্রদর্শনের উদ্দেশ্যে সিন্থেটিক ডেটা ব্যবহার করা হয়েছে',
    'educational_point_3': 'শিক্ষাগত স্বচ্ছতার জন্য মডেলগুলো সরলীকৃত',
    'educational_point_4': 'চিকিৎসা পরামর্শের জন্য সর্বদা যোগ্য স্বাস্থ্য পেশাদারের সাথে পরামর্শ করুন',
    'future_extensions_heading': 'ভবিষ্যৎ সম্প্রসারণ',
    'future_1': 'ওয়্যারেবল ডিভাইস (স্মার্টওয়াচ, ফিটনেস ট্র্যাকার) এর সাথে সংযুক্তি',
    'future_2': 'রিয়েল-টাইম সেন্সর ডেটা প্রসেসিং',
    'future_3': 'বিশ্বব্যাপী প্রবেশযোগ্যতার জন্য বহু-ভাষা সমর্থন',
    'future_4': 'চলতি পথে পর্যবেক্ষণের জন্য মোবাইল অ্যাপ্লিকেশন',
    'future_5': 'উন্নত নির্ভুলতার জন্য উন্নত ডিপ লার্নিং মডেল',
    'future_6': 'দূরবর্তী পরামর্শের জন্য টেলিমেডিসিন ইন্টিগ্রেশন',
    'future_7': 'প্রবেশযোগ্যতার জন্য ভয়েস-সক্রিয় ইন্টারফেস',
    'technology_stack_heading': 'প্রযুক্তি স্ট্যাক',
    'tech_backend': 'ব্যাকএন্ড',
    'tech_frontend': 'ফ্রন্টএন্ড',
    'tech_visualization': 'ভিজ্যুয়ালাইজেশন',
    'tech_storage': 'স্টোরেজ',
    'tech_storage_value': 'লোকাল ফাইল সিস্টেম (JSON)'
})

# Ensure all languages also receive newly added English keys.
for lang_code in SUPPORTED_LANGUAGES:
    for key, value in TRANSLATIONS['en'].items():
        TRANSLATIONS[lang_code].setdefault(key, value)

# Quality fallback: where selected regional dictionaries still equal English,
# prefer Hindi phrasing while preserving explicit native entries.
QUALITY_FALLBACK_LANGS = ['mr', 'ta', 'kn', 'te', 'or', 'pa', 'hry', 'gu', 'bho', 'ur']
for lang_code in QUALITY_FALLBACK_LANGS:
    for key, en_value in TRANSLATIONS['en'].items():
        if TRANSLATIONS.get(lang_code, {}).get(key) == en_value and key in TRANSLATIONS['hi']:
            TRANSLATIONS[lang_code][key] = TRANSLATIONS['hi'][key]

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
    patient_id = (patient_id or '').upper().strip()
    file_mapping = {
        '1D55PL6': 'patient_A.json',
        '7D42PL2': 'patient_B.json'
    }
    if patient_id in file_mapping:
        return file_mapping[patient_id]

    # Dynamically resolve all other seeded patients (e.g., C-L) from JSON files.
    patients_dir = os.path.join(DATA_DIR, 'patients')
    if os.path.exists(patients_dir):
        for fname in os.listdir(patients_dir):
            if not fname.endswith('.json'):
                continue
            fpath = os.path.join(patients_dir, fname)
            try:
                with open(fpath, 'r') as f:
                    pdata = json.load(f)
                if str(pdata.get('patient_id', '')).upper() == patient_id:
                    return fname
            except (json.JSONDecodeError, OSError):
                continue

    return f'patient_{patient_id}.json'


def _get_report_prefix(patient: dict, patient_id: str) -> str:
    """Derive report prefix like A/B/C from existing records or filename."""
    reports = patient.get('reports', []) if isinstance(patient, dict) else []
    for report in reports:
        report_id = report.get('report_id', '')
        if '_' in report_id:
            prefix = report_id.split('_', 1)[0].strip()
            if prefix:
                return prefix

    filename = _get_patient_filename(patient_id)
    stem = os.path.splitext(os.path.basename(filename))[0]
    if stem.startswith('patient_') and len(stem) > len('patient_'):
        return stem[len('patient_'):].upper()

    return (patient_id or 'P').upper()


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
    data = request.json or {}
    patient_id = data.get('patient_id', '').upper()
    password = data.get('password', '')

    patient_data = load_patient_data(patient_id)
    if patient_data and patient_data.get('password', '') == password:
        session['patient_id'] = str(patient_data.get('patient_id', patient_id)).upper()
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
    report_prefix = _get_report_prefix(patient, patient_id)
    report_id = f"{report_prefix}_R{next_index:03d}"

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
    report_prefix = _get_report_prefix(patient, patient_id)
    report_id = f"{report_prefix}_U{next_index:03d}"

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
        # Respect currently selected UI language for generated texts.
        current_lang = session.get('lang', DEFAULT_LANGUAGE)

        # Run all predictions
        predictions = inference_engine.predict_all(report_data)
        
        # Get recommendations
        recommendations = get_all_recommendations(predictions, current_lang)
        
        # Get summary message
        summary = get_summary_message(predictions, current_lang)
        
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