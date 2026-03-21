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
    },
    'bn': {
        'app_name': 'RehabSense', 'nav_home': 'হোম', 'nav_dashboard': 'ড্যাশবোর্ড', 'nav_progress': 'উন্নতি', 'nav_contact': 'যোগাযোগ', 'nav_logout': 'লগ আউট', 'nav_login': 'লগইন', 'hero_title': 'RehabSense', 'hero_tagline': 'আপনার স্মার্ট পুনর্বাসন সহায়ক', 'get_started': 'শুরু করুন', 'about_heading': 'RehabSense সম্পর্কে', 'login_options': 'লগইন অপশন', 'login_as_patient': 'রোগী হিসেবে লগইন', 'login_as_admin': 'অ্যাডমিন হিসেবে লগইন', 'patient_id': 'রোগীর আইডি', 'password': 'পাসওয়ার্ড', 'submit': 'লগইন', 'invalid_credentials': 'অবৈধ রোগী আইডি অথবা পাসওয়ার্ড।', 'welcome': 'স্বাগতম', 'your_health_reports': 'আপনার স্বাস্থ্য রিপোর্ট', 'view_details': 'বিস্তারিত দেখুন', 'view_progress': 'সময়ের সাথে উন্নতি দেখুন', 'admin_dashboard': 'অ্যাডমিন ড্যাশবোর্ড', 'language': 'ভাষা', 'about_para1': 'পুনর্বাসন রোগীদের প্রায়ই ক্রমাগত, বহু-প্যারামিটার পর্যবেক্ষণের প্রয়োজন স্থিতিশীল পুনরুদ্ধার নিশ্চিত করতে এবং জটিলতা প্রাথমিকভাবে সনাক্ত করতে। তবে বেশিরভাগ বিদ্যমান সমাধান শুধুমাত্র হৃদস্পন্দন, মুদ্রা বা গ্লুকোজ স্তরের মতো স্বাস্থ্যের একটি দিক সম্বোধন করে, যার ফলে খণ্ডিত যত্ন হয়।', 'about_para2': 'RehabSense একটি ইউনিফাইড, বুদ্ধিমান, মাল্টি-মোডাল স্বাস্থ্য পর্যবেক্ষণ প্ল্যাটফর্মের মাধ্যমে এই ব্যবধান পূরণ করার জন্য ডিজাইন করা হয়েছে। এটি প্রধান স্বাস্থ্য সূচকগুলির বিশ্লেষণকে একীভূত করে, যার মধ্যে হৃদস্পন্দনের অনিয়ম, অনুমানিত রক্ত গ্লুকোজ প্রবণতা, শ্বাসপ্রশ্বাসের প্যাটার্ন, বক্তৃতা বৈশিষ্ট্য, আবেগের স্থিতি এবং মুদ্রা রয়েছে একটি সমন্বিত সিস্টেমে।', 'about_para3': 'RehabSense-এর একটি মূল বৈশিষ্ট্য হল এর রিয়েল-টাইম, ভিডিও-ভিত্তিক মুদ্রা সনাক্তকরণ, যা বিশেষায়িত হার্ডওয়্যারের প্রয়োজন ছাড়াই শরীরের সারিবদ্ধতা এবং আন্দোলনের নির্ভুল ট্র্যাকিং সক্ষম করে।', 'about_para4': 'প্ল্যাটফর্মটি একটি ব্যবহারকারী-বান্ধব ওয়েব ইন্টারফেসও প্রদান করে যেখানে রোগীরা স্বাস্থ্য ডেটা লগ করতে, ঐতিহাসিক রেকর্ড অ্যাক্সেস করতে এবং স্বজ্ঞাত বিশ্লেষণের মাধ্যমে অগ্রগতি দেখাতে পারেন।', 'service1_title': 'রিয়েল-টাইম ডায়াগনসিস পান', 'service1_desc': 'আমাদের উন্নত এআই-চালিত পর্যবেক্ষণ সিস্টেমের মাধ্যমে ইন্টারেক্টিভ চার্ট এবং সম্পূর্ণ অস্বাভাবিকতা সনাক্তকরণ সহ তাৎক্ষণিক স্বাস্থ্য বিশ্লেষণ অনুভব করুন।', 'service2_title': 'দুর্দান্ত ভিজ্যুয়াল এবং চার্ট', 'service2_desc': 'স্বজ্ঞাত ভিজ্যুয়ালাইজেশন সহ আপনার স্বাস্থ্য অন্তর্দৃষ্টি সুন্দরভাবে বুঝুন এবং সম্পূর্ণ, সহজ-পাঠযোগ্য চার্টের সাথে আপনার পুনর্বাসন অগ্রগতি ট্র্যাক করুন।', 'service3_title': 'রিয়েল-টাইম সুপারিশ', 'service3_desc': 'আপনার নির্দিষ্ট স্বাস্থ্য অবস্থা এবং পুনরুদ্ধার লক্ষ্যের জন্য কাস্টমাইজ করা ব্যক্তিগত ব্যায়াম রুটিন, খাদ্যতালিকাগত নির্দেশনা এবং ডাক্তারের পরামর্শ পান।', 'service4_title': 'বহুভাষিক সমর্থন', 'service4_desc': 'আপনার পছন্দের ভাষায় আমাদের প্ল্যাটফর্মে অ্যাক্সেস করুন সম্পূর্ণ বহুভাষিক সমর্থনের সাথে, যা ভাষার বাধা নির্বিশেষে সবার জন্য স্বাস্থ্যসেবা প্রবেশযোগ্য করে তোলে।', 'our_services': 'আমাদের সেবা', 'educational_prototype': 'শিক্ষামূলক প্রোটোটাইপ শুধুমাত্র', 'disclaimer': 'এই সিস্টেম প্রদর্শনের উদ্দেশ্যে এবং চিকিৎসাগত পরামর্শ প্রদান করে না। চিকিৎসাগত সিদ্ধান্তের জন্য সর্বদা যোগ্য স্বাস্থ্যসেবা পেশাদারদের পরামর্শ করুন।', 'copyright': '© 2026 RehabSense - এআই পুনর্বাসন পর্যবেক্ষণ সিস্টেম', 'status_normal': 'সাধারণ', 'status_bradycardia': 'ব্র্যাডিকার্ডিয়া', 'status_tachycardia': 'ট্যাকিকার্ডিয়া', 'status_irregular': 'অনিয়মিত', 'status_low': 'কম', 'status_high': 'উচ্চ', 'status_shallow_breathing': 'অগভীর শ্বাস', 'status_apnea_risk': 'অ্যাপনিয়া ঝুঁকি', 'status_normal_speech': 'সাধারণ বক্তৃতা', 'status_slurred_speech': 'অস্পষ্ট/ধীর', 'status_stressed_speech': 'চাপপূর্ণ বক্তৃতা', 'status_happy': 'খুশি', 'status_neutral': 'নিরপেক্ষ', 'status_stressed': 'চাপপূর্ণ', 'status_sad': 'দুঃখী', 'status_good_posture': 'ভাল মুদ্রা', 'status_forward_head': 'এগিয়ে যাওয়া মাথার মুদ্রা', 'status_slouched': 'খোঁড়া বসা'
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