"""
Recommendation Engine
Provides personalized rehabilitation recommendations based on AI predictions
"""

# Translation dictionary for recommendations content
RECOMMENDATIONS_TRANSLATIONS = {
    'en': {
        'heart_health': 'Heart Health',
        'blood_glucose': 'Blood Glucose',
        'breathing_health': 'Breathing Health',
        'speech_communication': 'Speech & Communication',
        'emotional_wellbeing': 'Emotional Wellbeing',
        'posture_health': 'Posture Health',
        # Heartbeat
        'continue_moderate_aerobic': 'Continue moderate aerobic exercise (20-30 min, 3-4 times/week)',
        'walking_swimming_cycling': 'Walking, swimming, or cycling at comfortable pace',
        'maintain_current_healthy': 'Maintain current healthy habits',
        'stay_hydrated': 'Stay hydrated throughout the day',
        'heart_rhythm_healthy': 'Your heart rhythm is healthy!',
        'keep_up_good_work': 'Keep up the good work with regular activity',
        'light_aerobic_activities': 'Light aerobic activities to gradually increase heart rate',
        'gentle_walking_15_20': 'Gentle walking for 15-20 minutes daily',
        'stretching_flexibility': 'Stretching and flexibility exercises',
        'avoid_sudden_intense': 'Avoid sudden intense activities',
        'stay_warm_comfortable': 'Stay warm and comfortable',
        'monitor_feel_activities': 'Monitor how you feel during activities',
        'slow_heart_rate_detected': 'Slow heart rate detected - speak with your healthcare provider',
        'gradual_increase_activity': 'Gradual increase in activity is key',
        'gentle_breathing_exercises': 'Gentle breathing exercises',
        'slow_paced_yoga_tai_chi': 'Slow-paced yoga or tai chi',
        'avoid_high_intensity': 'Avoid high-intensity workouts temporarily',
        'reduce_caffeine_intake': 'Reduce caffeine intake',
        'practice_stress_management': 'Practice stress management',
        'ensure_adequate_rest': 'Ensure adequate rest and sleep',
        'elevated_heart_rate': 'Elevated heart rate detected',
        'focus_relaxation_calm': 'Focus on relaxation and calm activities',
        'low_impact_activities': 'Low-impact activities under supervision',
        'seated_exercises_gentle': 'Seated exercises and gentle movements',
        'avoid_strenuous': 'Avoid strenuous activities',
        'monitor_heart_rate': 'Monitor heart rate regularly',
        'consult_healthcare': 'Consult healthcare provider',
        'keep_symptom_diary': 'Keep a symptom diary',
        'irregular_rhythm_detected': 'Irregular rhythm detected - medical consultation recommended',
        'gentle_activity_safest': 'Gentle activity is safest for now',
        # Glucose
        'regular_physical_activity': 'Regular physical activity (30 min, 5 days/week)',
        'mix_cardio_strength': 'Mix of cardio and strength training',
        'maintain_balanced_meals': 'Maintain balanced meals',
        'continue_healthy_eating': 'Continue healthy eating habits',
        'glucose_well_controlled': 'Glucose levels are well-controlled!',
        'keep_monitoring_active': 'Keep monitoring and staying active',
        'light_activity_after': 'Light activity after meals',
        'avoid_empty_stomach': 'Avoid exercising on empty stomach',
        'eat_small_frequent': 'Eat small, frequent meals',
        'keep_healthy_snacks': 'Keep healthy snacks available',
        'monitor_blood_sugar': 'Monitor blood sugar before activities',
        'low_glucose_detected': 'Low glucose detected - ensure regular meals',
        'carry_quick_carbs': 'Carry quick-acting carbohydrates',
        'post_meal_walking': 'Post-meal walking (15-20 minutes)',
        'strength_training_2_3': 'Strength training 2-3 times per week',
        'focus_whole_foods': 'Focus on whole foods and vegetables',
        'limit_refined_carbs': 'Limit refined carbohydrates',
        'stay_well_hydrated': 'Stay well-hydrated',
        'elevated_glucose': 'Elevated glucose detected',
        'physical_activity_helps': 'Physical activity helps regulate blood sugar',
        # Breathing
        'deep_breathing_5_min': 'Deep breathing exercises (5 min daily)',
        'continue_current_activity': 'Continue current activity level',
        'good_air_quality': 'Maintain good air quality in living spaces',
        'stay_active_mobile': 'Stay active and mobile',
        'breathing_pattern_healthy': 'Breathing pattern is healthy!',
        'keep_practicing_breathing': 'Keep practicing good breathing habits',
        'diaphragmatic_breathing': 'Diaphragmatic breathing: Breathe deeply into belly (5-10 min, 3x/day)',
        'box_breathing': 'Box breathing: Inhale 4s, hold 4s, exhale 4s, hold 4s',
        'gentle_chest_expansion': 'Gentle chest expansion exercises',
        'good_posture_sitting': 'Practice good posture while sitting',
        'breathing_breaks_hour': 'Take breathing breaks every hour',
        'avoid_restrictive': 'Avoid restrictive clothing',
        'shallow_breathing_detected': 'Shallow breathing detected - focus on deep breaths',
        'lungs_hold_more_air': 'Your lungs can hold more air with practice',
        'paced_breathing': 'Paced breathing: Count to 4 on inhale, 6 on exhale',
        'relaxed_breathing_exercises': 'Relaxed breathing exercises',
        'gentle_yoga_breath': 'Gentle yoga focusing on breath',
        'reduce_stress_possible': 'Reduce stress where possible',
        'practice_mindfulness': 'Practice mindfulness',
        'monitor_breathing_patterns': 'Monitor breathing patterns',
        'irregular_breathing_noticed': 'Irregular breathing pattern noticed',
        'regular_practice_improves': 'Regular practice improves breathing rhythm',
        'breathing_awareness': 'Breathing awareness exercises',
        'gentle_aerobic_activity': 'Gentle aerobic activity',
        'consult_sleep_specialist': 'Consult sleep specialist',
        'sleep_on_side': 'Sleep on your side',
        'maintain_healthy_weight': 'Maintain healthy weight',
        'avoid_alcohol_bed': 'Avoid alcohol before bed',
        'potential_apnea_risk': 'Potential apnea risk - medical evaluation recommended',
        'good_sleep_position': 'Good sleep position helps breathing',
        # Speech
        'continue_conversation': 'Continue regular conversation practice',
        'reading_aloud_10': 'Reading aloud for 10 minutes daily',
        'stay_socially_engaged': 'Stay socially engaged',
        'maintain_communication': 'Maintain communication habits',
        'speech_patterns_healthy': 'Speech patterns are healthy!',
        'keep_practicing_communication': 'Keep practicing regular communication',
        'tongue_twisters_5': 'Tongue twisters practice (5 min daily)',
        'exaggerate_mouth': 'Exaggerate mouth movements when speaking',
        'reading_slowly_clearly': 'Reading aloud slowly and clearly',
        'facial_muscle_exercises': 'Facial muscle exercises',
        'speak_slowly_deliberately': 'Speak slowly and deliberately',
        'take_pauses_sentences': 'Take pauses between sentences',
        'speech_clarity_exercises': 'Speech clarity exercises will help',
        'practice_makes_perfect': 'Practice makes perfect - be patient with yourself',
        'breathing_before_speaking': 'Breathing exercises before speaking',
        'speak_slower_pace': 'Practice speaking at slower pace',
        'relaxation_techniques': 'Relaxation techniques',
        'mindful_communication': 'Mindful communication practice',
        'take_breaks_conversations': 'Take breaks during conversations',
        'stress_affects_speech': 'Stress affects speech - relaxation helps',
        'deep_breaths_speaking': 'Deep breaths before speaking can help',
        # Emotion
        'wonderful_emotional': 'Wonderful emotional state!',
        'positive_energy_valuable': 'Your positive energy is valuable',
        'engage_enjoyable_activities': 'Engage in enjoyable activities',
        'try_something_new': 'Try something new this week',
        'physical_exercise_mood': 'Physical exercise (boosts mood)',
        'connect_friends_family': 'Connect with friends or family',
        'practice_gratitude_daily': 'Practice gratitude daily',
        'spend_time_hobbies': 'Spend time on hobbies',
        'neutral_state_normal': 'Neutral state is normal',
        'small_activities_boost': 'Small activities can boost your mood',
        'deep_breathing_10': 'Deep breathing exercises (10 min, 2-3x/day)',
        'progressive_muscle': 'Progressive muscle relaxation',
        'nature_walks': 'Nature walks',
        'prioritize_sleep_7_9': 'Prioritize sleep (7-9 hours)',
        'limit_screen_time': 'Limit screen time before bed',
        'talk_someone_trust': 'Talk to someone you trust',
        'break_tasks_steps': 'Break tasks into smaller steps',
        'stress_manageable': 'Stress is manageable with the right tools',
        'be_kind_yourself': 'Be kind to yourself during difficult times',
        'light_physical_walks': 'Light physical activity (walks, gentle exercise)',
        'creative_expression': 'Creative expression (art, music, writing)',
        'reach_supportive': 'Reach out to supportive people',
        'maintain_routine': 'Maintain routine where possible',
        'speak_counselor': 'Consider speaking with a counselor',
        'achievable_tasks': 'Engage in small, achievable tasks',
        'feelings_valid_temporary': 'These feelings are valid and temporary',
        'support_available': 'Support is available - you don\'t have to go through this alone',
        # Posture
        'core_strengthening': 'Continue core strengthening exercises',
        'maintain_flexibility': 'Maintain flexibility with stretching',
        'good_posture_habits': 'Keep practicing good posture habits',
        'movement_breaks': 'Take movement breaks regularly',
        'excellent_posture': 'Excellent posture!',
        'maintaining_prevents': 'Maintaining good posture prevents future issues',
        'chin_tucks_10': 'Chin tucks: Pull chin back (10 reps, 3x/day)',
        'neck_stretches': 'Neck stretches: Gentle side-to-side and up-down',
        'upper_back_strengthening': 'Upper back strengthening: Rows and reverse flies',
        'chest_stretches_30': 'Chest stretches: Doorway stretch (30s, 3 reps)',
        'adjust_screen_height': 'Adjust screen height to eye level',
        'ergonomic_workspace': 'Use ergonomic workspace setup',
        'posture_check_reminders': 'Set posture check reminders',
        'avoid_prolonged_phone': 'Avoid prolonged phone use',
        'forward_very_common': 'Forward head posture is very common with screen use',
        'small_adjustments_big': 'Small adjustments make big differences',
        'core_exercises_planks': 'Core exercises: Planks, bridges (daily)',
        'back_extensions_superman': 'Back extensions: Superman pose (10 reps, 2 sets)',
        'hip_flexor_stretches': 'Hip flexor stretches (30s each side)',
        'shoulder_blade_squeezes': 'Shoulder blade squeezes (15 reps, 3x/day)',
        'use_lumbar_support': 'Use lumbar support when sitting',
        'stand_up_30_minutes': 'Stand up every 30 minutes',
        'adjust_chair_height': 'Adjust chair height properly',
        'sit_tall_shoulders': 'Practice sitting tall with shoulders back',
        'slouching_stress_spine': 'Slouching puts stress on your spine',
        'building_core_strength': 'Building core strength helps maintain posture',
        # Summary message parts
        'great_job_maintaining': 'Great job maintaining',
        'focus_areas_improvement': 'Focus areas for improvement',
        'follow_recommendations': 'Follow the recommendations below to support your rehabilitation journey.',
        'keep_up_rehabilitation': 'Keep up your rehabilitation activities and monitor your progress.',
        'continue_healthy_stay': 'Continue your healthy habits and stay consistent with your routine.',
    },
    'hi': {
        'heart_health': 'हृदय स्वास्थ्य',
        'blood_glucose': 'रक्त शर्करा',
        'breathing_health': 'श्वसन स्वास्थ्य',
        'speech_communication': 'भाषण और संचार',
        'emotional_wellbeing': 'भावनात्मक कल्याण',
        'posture_health': 'मुद्रा स्वास्थ्य',
        'continue_moderate_aerobic': 'मध्यम हृदय व्यायाम (20-30 मिनट, सप्ताह में 3-4 बार) जारी रखें',
        'walking_swimming_cycling': 'आरामदायक गति से चलना, तैराकी या साइकिल चलाना',
        'maintain_current_healthy': 'अपनी वर्तमान स्वस्थ आदतें बनाए रखें',
        'stay_hydrated': 'दिनभर हाइड्रेटेड रहें',
        'heart_rhythm_healthy': 'आपकी हृदय गति स्वस्थ है!',
        'keep_up_good_work': 'नियमित गतिविधि के साथ अच्छा काम करते रहें',
        'great_job_maintaining': 'जो आप बनाए रख रहे हैं उसके लिए बहुत अच्छा काम',
        'focus_areas_improvement': 'सुधार के क्षेत्र',
        'follow_recommendations': 'आपकी पुनर्वास यात्रा का समर्थन करने के लिए नीचे दी गई सिफारिशों का पालन करें।',
        'keep_up_rehabilitation': 'अपनी पुनर्वास गतिविधियां जारी रखें और अपनी प्रगति की निगरानी करें।',
        'continue_healthy_stay': 'अपनी स्वस्थ आदतें जारी रखें और अपनी दिनचर्या के साथ सुसंगत रहें।',
    },
    # Spanish - Español
    'es': {
        'heart_health': 'Salud del Corazón',
        'blood_glucose': 'Glucosa en Sangre',
        'breathing_health': 'Salud Respiratoria',
        'speech_communication': 'Habla y Comunicación',
        'emotional_wellbeing': 'Bienestar Emocional',
        'posture_health': 'Salud Postural',
        'continue_moderate_aerobic': 'Continúa con ejercicio aeróbico moderado (20-30 min, 3-4 veces/semana)',
        'walking_swimming_cycling': 'Caminar, nadar o andar en bicicleta a ritmo cómodo',
        'maintain_current_healthy': 'Mantén tus hábitos saludables actuales',
        'stay_hydrated': 'Mantente hidratado durante todo el día',
        'heart_rhythm_healthy': '¡Tu ritmo cardíaco es saludable!',
        'keep_up_good_work': 'Continúa con el buen trabajo con la actividad regular',
        'great_job_maintaining': 'Excelente trabajo manteniendo tu salud',
        'focus_areas_improvement': 'Áreas de mejora',
        'follow_recommendations': 'Sigue las recomendaciones a continuación para apoyar tu jornada de rehabilitación.',
        'keep_up_rehabilitation': 'Continúa con tus actividades de rehabilitación y monitorea tu progreso.',
        'continue_healthy_stay': 'Continúa con tus hábitos saludables y mantente consistente con tu rutina.',
    },
    # Bengali - বাংলা
    'bn': {
        'heart_health': 'হৃদয় স্বাস্থ্য',
        'blood_glucose': 'রক্তে গ্লুকোজ',
        'breathing_health': 'শ্বাসযন্ত্রের স্বাস্থ্য',
        'speech_communication': 'বক্তৃতা এবং যোগাযোগ',
        'emotional_wellbeing': 'আবেগজনক সুস্থতা',
        'posture_health': 'শারীরিক ভঙ্গি স্বাস্থ্য',
        'continue_moderate_aerobic': 'মধ্যম এয়ারোবিক ব্যায়াম অব্যাহত রাখুন (২০-৩০ মিনিট, সপ্তাহে ৩-৪ বার)',
        'walking_swimming_cycling': 'আরামদায়ক গতিতে হাঁটা, সাঁতার বা সাইকেল চালানো',
        'maintain_current_healthy': 'আপনার বর্তমান স্বাস্থ্যকর অভ্যাসগুলি বজায় রাখুন',
        'stay_hydrated': 'সারাদিন জলযুক্ত থাকুন',
        'heart_rhythm_healthy': 'আপনার হৃদস্পন্দন সুস্থ!',
        'keep_up_good_work': 'নিয়মিত কার্যকলাপের সাথে ভাল কাজ চালিয়ে যান',
        'great_job_maintaining': 'আপনার স্বাস্থ্য বজায় রাখার জন্য চমৎকার কাজ',
        'focus_areas_improvement': 'উন্নতির ক্ষেত্রগুলি',
        'follow_recommendations': 'আপনার পুনর্বাসন যাত্রাকে সমর্থন করার জন্য নীচের সুপারিশগুলি অনুসরণ করুন।',
        'keep_up_rehabilitation': 'আপনার পুনর্বাসন কার্যক্রম চালিয়ে যান এবং আপনার অগ্রগতি পর্যবেক্ষণ করুন।',
        'continue_healthy_stay': 'আপনার স্বাস্থ্যকর অভ্যাসগুলি চালিয়ে যান এবং আপনার রুটিনে সামঞ্জস্যপূর্ণ থাকুন।',
    },
    # Marathi - मराठी
    'mr': {
        'heart_health': 'हृदय आरोग्य',
        'blood_glucose': 'रक्त ग्लूकोज',
        'breathing_health': 'श्वसन आरोग्य',
        'speech_communication': 'भाषण आणि संचार',
        'emotional_wellbeing': 'भावनिक कल्याण',
        'posture_health': 'भाव आरोग्य',
        'continue_moderate_aerobic': 'मध्यम एरोबिक व्यायाम सुरू ठेवा (२०-३० मिनिटे, आठवड्यातून ३-४ वेळा)',
        'walking_swimming_cycling': 'आरामदायक गतीने चालणे, तरंगणे किंवा सायकल चालवणे',
        'maintain_current_healthy': 'आपल्या सद्य आरोग्यकर अभ्यासांची देखभाल करा',
        'stay_hydrated': 'दिनभर हायड्रेटेड राहा',
        'heart_rhythm_healthy': 'आपली हृदय गती आरोग्यकर आहे!',
        'keep_up_good_work': 'नियमित क्रियाकलापांसह चांगले काम सुरू ठेवा',
        'great_job_maintaining': 'आपल्या आरोग्यच्या देखभाल करण्योबद्दल उत्तम काम',
        'focus_areas_improvement': 'सुधारण्याचे क्षेत्र',
        'follow_recommendations': 'आपली पुनर्वसन यात्रा समर्थित करण्यासाठी खालील शिफारसी पालन करा।',
        'keep_up_rehabilitation': 'आपल्या पुनर्वसन कार्यक्रम सुरू ठेवा आणि आपल्या प्रगतीची निगरानी करा।',
        'continue_healthy_stay': 'आपल्या आरोग्यकर अभ्यास सुरू ठेवा आणि आपल्या दैनंदिन जीवनात सुसंगत राहा।',
    },
    # Tamil - தமிழ்
    'ta': {
        'heart_health': 'இதய ஆரோக்கியம்',
        'blood_glucose': 'இரத்த சர்க்கரை',
        'breathing_health': 'சுவாస ஆரோக்கியம்',
        'speech_communication': 'பேச்சு மற்றும் தொடர்பாடல்',
        'emotional_wellbeing': 'உணர்வு நல்நிலை',
        'posture_health': 'தோரணை ஆரோக்கியம்',
        'continue_moderate_aerobic': 'மிதமான எரோபிக் உடற்பயிற்சি தொடரவும் (20-30 நிமிடம், வாரத்தில் 3-4 முறை)',
        'walking_swimming_cycling': 'வசதியான வேகத்தில் நடத்தல், நீச்சல் அல்லது சைக்கிள் சவாரி',
        'maintain_current_healthy': 'உங்கள் தற்போதைய ஆரோக்கியமான பழக்கவழக்கங்களை பராமரிக்கவும்',
        'stay_hydrated': 'நாள் முழுவதும் நீரேற்றமாக இருங்கள்',
        'heart_rhythm_healthy': 'உங்கள் இதய துடிப்பு ஆரோக்கியமாக உள்ளது!',
        'keep_up_good_work': 'வழக்கமான செயல்பாட்டுடன் நல்ல பணியைத் தொடரவும்',
        'great_job_maintaining': 'உங்கள் ஆரோக்கியத்தை பராமரிக்க சிறந்த பணி',
        'focus_areas_improvement': 'மேம்பாட்டுக்கான பகுதிகள்',
        'follow_recommendations': 'உங்கள் மீள்ப்பயிற்சி பயணத்தை ஆதரிக்க கீழே உள்ள பரிந்துரைகளைப் பின்பற்றவும்.',
        'keep_up_rehabilitation': 'உங்கள் மீள்ப்பயிற்சி செயல்பாடுகளை தொடரவும் மற்றும் உங்கள் முன்னேற்றத்தைக் கண்காணிக்கவும்.',
        'continue_healthy_stay': 'உங்கள் ஆரோக்கியமான பழக்கவழக்கங்களைத் தொடரவும் மற்றும் உங்கள் ரুடினுடன் சரியான வகையில் இருங்கள்।',
    },
    # Kannada - ಕನ್ನಡ
    'kn': {
        'heart_health': 'ಹೃದಯ ಆರೋಗ್ಯ',
        'blood_glucose': 'ರಕ್ತ ಗ್ಲೂಕೋಸ್',
        'breathing_health': 'ಶ್ವಾಸಪ್ರಶ್ವಾಸ ಆರೋಗ್ಯ',
        'speech_communication': 'ಮಾತು ಮತ್ತು ಸಂವಹನ',
        'emotional_wellbeing': 'ಭಾವನೆಯ ಯೋಗಕ್ಷೇಮ',
        'posture_health': 'ಮುದ್ರೆಂಚ ಆರೋಗ್ಯ',
        'continue_moderate_aerobic': 'ಮಧ್ಯದಿಂದ ಏರೋಬಿಕ್ ವ್ಯಾಯಾಮ ಮುಂದುವರಿಸಿ (20-30 ನಿಮಿಷ, ವಾರಕ್ಕೆ 3-4 ಬಾರಿ)',
        'walking_swimming_cycling': 'ಆರಾಮದಾಯಕ ಲಯದಲ್ಲಿ ನಡೆಯುವುದು, ಈಜುವುದು ಅಥವಾ ಸೈಕಲ್ ಚಾಲನೆ',
        'maintain_current_healthy': 'ನಿಮ್ಮ ಪ್ರಸ್ತುತ ಆರೋಗ್ಯಕರ ಅಭ್ಯಾಸಗಳನ್ನು ಕಾಪಾಡಿಕೊಳ್ಳಿ',
        'stay_hydrated': 'ದಿನ ಸುದ್ಧಾ ಸಿದ್ಧಾರ್ಥನಾಗಿರಿ',
        'heart_rhythm_healthy': 'ನಿಮ್ಮ ಹೃದಯ ಬಡಿತ ಆರೋಗ್ಯಕರವಾಗಿದೆ!',
        'keep_up_good_work': 'ನಿಯಮಿತ ಕ್ರಿಯಾಶೀಲತೆಯೊಂದಿಗೆ ಉತ್ತಮ ಕೆಲಸ ಮುಂದುವರಿಸಿ',
        'great_job_maintaining': 'ನಿಮ್ಮ ಆರೋಗ್ಯ ನಿರ್ವಹಣೆಗಾಗಿ ಉತ್ತಮ ಕೆಲಸ',
        'focus_areas_improvement': 'ಭಿನ್ನತ್ವದ ಕ್ಷೇತ್ರಗಳು',
        'follow_recommendations': 'ನಿಮ್ಮ ಪುನರ್ವಸನ ಪ್ರವಾಸವನ್ನು ಬೆಂಬಲಿಸಲು ಕೆಳಗಿನ ಶಿಫಾರಸುಗಳನ್ನು ಅನುಸರಿಸಿ।',
        'keep_up_rehabilitation': 'ನಿಮ್ಮ ಪುನರ್ವಸನ ಚಟುವಟಿಕೆಗಳನ್ನು ಮುಂದುವರಿಸಿ ಮತ್ತು ನಿಮ್ಮ ಪ್ರಗತಿಯನ್ನು ಮೇಲ್ವಿವರಣೆ ಮಾಡಿ।',
        'continue_healthy_stay': 'ನಿಮ್ಮ ಆರೋಗ್ಯಕರ ಅಭ್ಯಾಸಗಳನ್ನು ಮುಂದುವರಿಸಿ ಮತ್ತು ನಿಮ್ಮ ದಿನನಿತ್ಯದೊಂದಿಗೆ ಸುಸಂಗತವಾಗಿ ಉಳಿಯಿರಿ।',
    },
    # Telugu - తెలుగు
    'te': {
        'heart_health': 'గుండె ఆరోగ్యం',
        'blood_glucose': 'రక్త గ్లూకోజ్',
        'breathing_health': 'శ్వాస ఆరోగ్యం',
        'speech_communication': 'ప్రసంగ మరియు సంప్రేషణ',
        'emotional_wellbeing': 'ఉద్వేగ సుఖం',
        'posture_health': 'భంగిమ ఆరోగ్యం',
        'continue_moderate_aerobic': 'మితమైన ఏరోబిక్ వ్యాయామం కొనసాగించండి (20-30 నిమిషాలు, వారానికి 3-4 సార్లు)',
        'walking_swimming_cycling': 'సౌకర్య వేగంలో నడకడం, ఈత వేయడం లేదా సైకిల్ సవారీ',
        'maintain_current_healthy': 'మీ ప్రస్తుత ఆరోగ్యకర అలవాట్లను కొనసాగించండి',
        'stay_hydrated': 'రోజంతా జలయುక్తంగా ఉండండి',
        'heart_rhythm_healthy': 'మీ గుండె కొట్టడం ఆరోగ్యకరంగా ఉంది!',
        'keep_up_good_work': 'సాధారణ కార్యকలాపాలతో మంచి పనిని కొనసాగించండి',
        'great_job_maintaining': 'మీ ఆరోగ్యం నిర్వహణ చేయడానికి గొప్ప పని',
        'focus_areas_improvement': 'సుధారణ ప్రాంతాలు',
        'follow_recommendations': 'మీ పుনరుద్ధరణ ప్రయాణానికి సహాయం చేయడానికి దిగువ సిఫారసులను అనుసరించండి.',
        'keep_up_rehabilitation': 'మీ పునరుద్ధరణ కార్యకలాపాలను కొనసాగించండి మరియు మీ ప్రగతిని పర్యవేక్షించండి.',
        'continue_healthy_stay': 'మీ ఆరోగ్యకర అలవాట్లను కొనసాగించండి మరియు మీ దినచర్యతో సంగతిగా ఉండండి.',
    },
    # Odia - ଓଡିଆ
    'or': {
        'heart_health': 'ହାୱାର୍ଟ ସ୍ୱାସ୍ଥ୍ୟ',
        'blood_glucose': 'ରକ୍ତ ଗ୍ଲୁକୋଜ',
        'breathing_health': 'ଶ୍ବସନ ସ୍ୱାସ୍ଥ୍ୟ',
        'speech_communication': 'ବାକ୍ୟ ଓ ଯୋଗାଯୋଗ',
        'emotional_wellbeing': 'ମାନସିକ ସୁସ୍ଥ',
        'posture_health': 'ମୁଦ୍ରା ସ୍ୱାସ୍ଥ୍ୟ',
        'continue_moderate_aerobic': 'ମାଧ୍ୟମିକ ଏରୋବିକ୍ ବ୍ୟାୟାମ ଜାରି ରଖନ୍ତୁ (20-30 ମିନିଟ, ସପ୍ତାହରେ 3-4 ଥର)',
        'walking_swimming_cycling': 'ଆରାମଦାୟକ ଗତିରେ ଚାଲିବା, ସାଁତାରିବା କିମ୍ବା ସାଇକେଲ ଚଲାଇବା',
        'maintain_current_healthy': 'ତୁମର ବର୍ତ୍ତମାନର ସୁସ୍ଥ ଅଭ୍ୟାସ ବଜାୟ ରଖ',
        'stay_hydrated': 'ଦିନ ଭର ଜଳୀୟ ରୁହ',
        'heart_rhythm_healthy': 'ତୁମର ହୃଦୟ ଗତି ସୁସ୍ଥ!',
        'keep_up_good_work': 'ନିୟମିତ କାର୍ଯ୍ୟକଲାପ ସହ ଭାଲକାମ ଜାରି ରଖ',
        'great_job_maintaining': 'ତୁମର ସ୍ୱାସ୍ଥ୍ୟ ରକ୍ଷାକରିବାରେ ଭଲ କାମ',
        'focus_areas_improvement': 'ଉନ୍ନତି ଏଲାକା',
        'follow_recommendations': 'ତୁମର ପୁନର୍ବାସନ ଯାତ୍ରା ସମର୍ଥନ କରିବାକୁ କ୍ଷେତ୍ର ସୁପାରିସ ଅନୁସରଣ କର।',
        'keep_up_rehabilitation': 'ତୁମର ପୁନର୍ବାସନ କାର୍ଯ୍ୟକଲାପ ଜାରି ରଖ ଓ ତୁମର ଅଗ୍ରଗତି ପର୍ଯ୍ୟବେକ୍ଷଣ କର।',
        'continue_healthy_stay': 'ତୁମର ସୁସ୍ଥ ଅଭ୍ୟାସ ଜାରି ରଖ ଓ ତୁମର ଦୈନନ୍ଦିନ ଜୀବନରେ ସଂଗତିପୂର୍ଣ୍ଣ ରୁହ।',
    },
    # Punjabi - ਪੂਜਾਬੀ
    'pa': {
        'heart_health': 'ਦਿਲ ਦੀ ਸਿਹਤ',
        'blood_glucose': 'ਖੂਨ ਵਿਚ ਸ਼ੂਗਰ',
        'breathing_health': 'ਸਾਹ ਲੈਣ ਦੀ ਸਿਹਤ',
        'speech_communication': 'ਬੋਲੀ ਅਤੇ ਸੰਚਾਰ',
        'emotional_wellbeing': 'ਭਾਵਨਾਤਮਕ ਸੁਖ',
        'posture_health': 'ਮੁੰਡਾ ਸਿਹਤ',
        'continue_moderate_aerobic': 'ਮਿਆਰੀ ਏਰੋਬਿਕ ਕਸਰਤ ਜਾਰੀ ਰੱਖੋ (20-30 ਮਿੰਟ, ਹਫ਼ਤਾ 3-4 ਬਾਰ)',
        'walking_swimming_cycling': 'ਅਰਾਮ ਦੀ ਰਫ਼ਤਾਰ ਵਿਚ ਚੱਲਣਾ, ਤਰਨਾ ਜਾਂ ਸਾਈਕਿਲ ਚੱਲਾਉਣਾ',
        'maintain_current_healthy': 'ਆਪਣੀਆ ਮੌਜੂਦਾ ਸਿਹਤਮੰਦ ਆਦਤਾ ਬਰਕਰਾਰ ਰਖੋ',
        'stay_hydrated': 'ਸਾਰੇ ਦਿਨ ਪਾਣੀ ਪੀਤੇ ਰਹੋ',
        'heart_rhythm_healthy': 'ਤੁਹਾਡੀ ਦਿਲ ਦੀ ਧੜਕਨ ਸਿਹਤਮੰਦ ਹੈ!',
        'keep_up_good_work': 'ਨਿਯਮਤ ਕਾਰਜਕਲਾਪ ਨਾਲ ਵਧੀਆ ਕੰਮ ਕਰੋ',
        'great_job_maintaining': 'ਤੁਹਾਡੀ ਸਿਹਤ ਬਰਕਰਾਰ ਰਾਖਣ ਵਾਸਤੇ ਬਹੁ ਖੂਬ',
        'focus_areas_improvement': 'ਬਿਹਤਰੀ ਦੇ ਖੇਤਰ',
        'follow_recommendations': 'ਆਪਣੀ ਪੁਨਰਵਾੱਸ ਯਾਤਰਾ ਸਥਾਪਤ ਕਰਨ ਲਈ ਹੇਠਾ ਦੀਆਂ ਸਫ਼ਾਰਸ਼ਾ ਅਮਲ ਵਿਚ ਲਾਓ।',
        'keep_up_rehabilitation': 'ਆਪਣੀ ਪੁਨਰਵਾੱਸ ਗਤੀਵਿਧੀਆਂ ਜਾਰੀ ਰਾਖੋ ਅਤੇ ਆਪਣੀ ਤਰੱਕੀ ਮੌਨੀਟਰ ਕਰੋ।',
        'continue_healthy_stay': 'ਆਪਣੀਆ ਸਿਹਤਮੰਦ ਆਦਤਾ ਜਾਰੀ ਰੱਖੋ ਅਤੇ ਆਪਣੀ ਪ੍ਰੋਗ੍ਰਾਮ ਨਾਲ ਬਰਾਬਰੀ ਕਰੋ।',
    },
    # Haryanvi - हरियाणवी
    'hry': {
        'heart_health': 'दिल की सेहत',
        'blood_glucose': 'खून में शुगर',
        'breathing_health': 'सांस की सेहत',
        'speech_communication': 'बोली ओ संचार',
        'emotional_wellbeing': 'भावनात्मक सुख',
        'posture_health': 'मुंडा सेहत',
        'continue_moderate_aerobic': 'मियारी एरोबिक कसरत जारी राखो (20-30 मिनट, हफ्ता 3-4 बार)',
        'walking_swimming_cycling': 'राम की रफ्तार में चलणा, तैरणा या साइकिल चलाणा',
        'maintain_current_healthy': 'अपणी मौजूदा सिहतमंद आदतां बरकरार राखो',
        'stay_hydrated': 'सारे दिन पानी पीते रहो',
        'heart_rhythm_healthy': 'तुम्हारी दिल की धड़कन सिहतमंद है!',
        'keep_up_good_work': 'नियमत कारजकलाप नाल वढिया काम करो',
        'great_job_maintaining': 'तुम्हारी सिहत बरकरार राखणे वास्ते बोहत खूब',
        'focus_areas_improvement': 'बिहतरी के खेत',
        'follow_recommendations': 'अपणी पुनरवास यात्रा समर्थित करणे लिए हेठा दीण सफारसां अमल में लाओ।',
        'keep_up_rehabilitation': 'अपणी पुनरवास गतीविधीयां जारी राखो ओ अपणी तरक्की मोनिटर करो।',
        'continue_healthy_stay': 'अपणी सिहतमंद आदतां जारी राखो ओ अपणी प्रोग्राम नाल बराबरी करो।',
    },
    # Gujarati - ગુજરાતી
    'gu': {
        'heart_health': 'હૃદય આરોગ્ય',
        'blood_glucose': 'રક્ત ગ્લુકોજ',
        'breathing_health': 'શ્વાસ આરોગ્ય',
        'speech_communication': 'વાણી અને સંચાર',
        'emotional_wellbeing': 'આવેગજનક કલ્યાણ',
        'posture_health': 'મુદ્રા આરોગ્ય',
        'continue_moderate_aerobic': 'મધ્યમ એરોબિક વ્યાયામ ચાલુ રાખો (20-30 મિનિટ, અઠવાડિયે 3-4 વખત)',
        'walking_swimming_cycling': 'આરામદાયક ગતીથી ચાલવું, તરવું અથવા સાઇકલ ચલાવવી',
        'maintain_current_healthy': 'તમારી વર્તમાન આરોગ્યકર આદતો જાળવી રાખો',
        'stay_hydrated': 'દિવસ ભર હાઇડ્રેટેડ રહો',
        'heart_rhythm_healthy': 'તમારી હૃદય ધબકણ આરોગ્યકર છે!',
        'keep_up_good_work': 'નિયમિત પ્રવૃત્તિ સાથે સારું કામ ચાલુ રાખો',
        'great_job_maintaining': 'તમારા આરોગ્યની જાળવણી કરવા માટે બહુ સારું કામ',
        'focus_areas_improvement': 'સુધારણા ક્ષેત્રો',
        'follow_recommendations': 'તમારી પુનર્વસન યાત્રાને સહાય આપવા માટે નીચેની ભલામણ અનુસરો।',
        'keep_up_rehabilitation': 'તમારી પુનર્વસન પ્રવૃત્તિ ચાલુ રાખો અને તમારી પ્રગતির દેખરેખ રાખો।',
        'continue_healthy_stay': 'તમારી આરોગ્યકર આદતો ચાલુ રાખો અને તમારી દૈનંદિન જીવન સાથે સુસંગત રહો।',
    },
    # Bhojpuri - भोजपुरी
    'bho': {
        'heart_health': 'दिल के सेहत',
        'blood_glucose': 'खून में शुगर',
        'breathing_health': 'सांस के सेहत',
        'speech_communication': 'बोली ओ संचार',
        'emotional_wellbeing': 'भावनात्मक सुख',
        'posture_health': 'मुंडा सेहत',
        'continue_moderate_aerobic': 'मध्यम एरोबिक कसरत चलावत रहो (20-30 मिनट, हफ्ता 3-4 बार)',
        'walking_swimming_cycling': 'राम के रफ्तार में चलत, तैरत या साइकिल चलावत',
        'maintain_current_healthy': 'अपन के मौजूद सेहतमंद आदत बनावत राख',
        'stay_hydrated': 'सारे दिन पानी पीत रहो',
        'heart_rhythm_healthy': 'तुम्हार दिल के धड़कन सेहतमंद बा!',
        'keep_up_good_work': 'नियमत काम-काज के साथ अच्छा काम चलावत रहो',
        'great_job_maintaining': 'तुम्हार सेहत बनावत राखेसन के लिए बहुत अच्छा काम',
        'focus_areas_improvement': 'सुधार के इलाका',
        'follow_recommendations': 'अपन के पुनरवास यात्रा सहायता करे खातिर निचे दे गइल सफारस के पालन करो।',
        'keep_up_rehabilitation': 'अपन के पुनरवास गतीविधी चलावत रहो ओ अपन के तरक्की के निगरानी करो।',
        'continue_healthy_stay': 'अपन के सेहतमंद आदत चलावत रहो ओ अपन के दिनचर्या के साथ मेल बनावत रहो।',
    },
    # Urdu - اردو
    'ur': {
        'heart_health': 'دل کی صحت',
        'blood_glucose': 'خون میں شکر',
        'breathing_health': 'سانس کی صحت',
        'speech_communication': 'بات چیت اور مواصلات',
        'emotional_wellbeing': 'جذباتی خوشحالی',
        'posture_health': 'مستقل صحت',
        'continue_moderate_aerobic': 'اعتدال پسند ایروبک ورزش جاری رکھیں (20-30 منٹ، ہفتے میں 3-4 بار)',
        'walking_swimming_cycling': 'آرام سے چلنا، تیراکی یا سائیکل چلانا',
        'maintain_current_healthy': 'اپنی موجودہ صحت مند عادتوں کو برقرار رکھیں',
        'stay_hydrated': 'پورے دن ہائیڈریٹڈ رہیں',
        'heart_rhythm_healthy': 'آپ کی دل کی دھڑکن صحت مند ہے!',
        'keep_up_good_work': 'معمولی سرگرمی کے ساتھ اچھی کوشش جاری رکھیں',
        'great_job_maintaining': 'آپ کی صحت کو برقرار رکھنے کے لیے بہترین کام',
        'focus_areas_improvement': 'بہتری کے شعبے',
        'follow_recommendations': 'اپنی بحالی کی سفر کی حمایت کے لیے ذیل میں سفارشات پر عمل کریں۔',
        'keep_up_rehabilitation': 'اپنی بحالی کی سرگرمیوں کو جاری رکھیں اور اپنی ترقی کی نگرانی کریں۔',
        'continue_healthy_stay': 'اپنی صحت مند عادتوں کو جاری رکھیں اور اپنی روزمرہ کی زندگی سے متعلق رہیں۔',
    }
}

def get_heartbeat_recommendations(prediction, lang='en'):
    """Get recommendations for heartbeat abnormalities"""
    status = prediction['status']
    # Get language dict with fallback to English for missing keys
    lang_dict = RECOMMENDATIONS_TRANSLATIONS.get(lang, {})
    t = lambda key: lang_dict.get(key, RECOMMENDATIONS_TRANSLATIONS['en'].get(key, key))
    
    recommendations = {
        'title': t('heart_health'),
        'status': status,
        'exercises': [],
        'lifestyle': [],
        'tips': []
    }
    
    if status == 'Normal':
        recommendations['exercises'] = [
            t('continue_moderate_aerobic'),
            t('walking_swimming_cycling')
        ]
        recommendations['lifestyle'] = [
            t('maintain_current_healthy'),
            t('stay_hydrated')
        ]
        recommendations['tips'] = [
            t('heart_rhythm_healthy'),
            t('keep_up_good_work')
        ]
    
    elif status == 'Bradycardia':
        recommendations['exercises'] = [
            t('light_aerobic_activities'),
            t('gentle_walking_15_20'),
            t('stretching_flexibility')
        ]
        recommendations['lifestyle'] = [
            t('avoid_sudden_intense'),
            t('stay_warm_comfortable'),
            t('monitor_feel_activities')
        ]
        recommendations['tips'] = [
            t('slow_heart_rate_detected'),
            t('gradual_increase_activity')
        ]
    
    elif status == 'Tachycardia':
        recommendations['exercises'] = [
            t('gentle_breathing_exercises'),
            t('slow_paced_yoga_tai_chi'),
            t('avoid_high_intensity')
        ]
        recommendations['lifestyle'] = [
            t('reduce_caffeine_intake'),
            t('practice_stress_management'),
            t('ensure_adequate_rest')
        ]
        recommendations['tips'] = [
            t('elevated_heart_rate'),
            t('focus_relaxation_calm')
        ]
    
    elif status == 'Irregular':
        recommendations['exercises'] = [
            t('low_impact_activities'),
            t('seated_exercises_gentle'),
            t('avoid_strenuous')
        ]
        recommendations['lifestyle'] = [
            t('monitor_heart_rate'),
            t('consult_healthcare'),
            t('keep_symptom_diary')
        ]
        recommendations['tips'] = [
            t('irregular_rhythm_detected'),
            t('gentle_activity_safest')
        ]
    
    return recommendations

def get_glucose_recommendations(prediction, lang='en'):
    """Get recommendations for glucose management"""
    range_label = prediction['range']
    # Get language dict with fallback to English for missing keys
    lang_dict = RECOMMENDATIONS_TRANSLATIONS.get(lang, {})
    t = lambda key: lang_dict.get(key, RECOMMENDATIONS_TRANSLATIONS['en'].get(key, key))
    
    recommendations = {
        'title': t('blood_glucose'),
        'status': range_label,
        'exercises': [],
        'lifestyle': [],
        'tips': []
    }
    
    if range_label == 'Normal':
        recommendations['exercises'] = [
            t('regular_physical_activity'),
            t('mix_cardio_strength')
        ]
        recommendations['lifestyle'] = [
            t('maintain_balanced_meals'),
            t('continue_healthy_eating')
        ]
        recommendations['tips'] = [
            t('glucose_well_controlled'),
            t('keep_monitoring_active')
        ]
    
    elif range_label == 'Low':
        recommendations['exercises'] = [
            t('light_activity_after'),
            t('avoid_empty_stomach')
        ]
        recommendations['lifestyle'] = [
            t('eat_small_frequent'),
            t('keep_healthy_snacks'),
            t('monitor_blood_sugar')
        ]
        recommendations['tips'] = [
            t('low_glucose_detected'),
            t('carry_quick_carbs')
        ]
    
    elif range_label == 'High':
        recommendations['exercises'] = [
            t('post_meal_walking'),
            t('regular_physical_activity'),
            t('strength_training_2_3')
        ]
        recommendations['lifestyle'] = [
            t('focus_whole_foods'),
            t('limit_refined_carbs'),
            t('stay_well_hydrated')
        ]
        recommendations['tips'] = [
            t('elevated_glucose'),
            t('physical_activity_helps')
        ]
    
    return recommendations

def get_breathing_recommendations(prediction, lang='en'):
    """Get recommendations for breathing patterns"""
    status = prediction['status']
    # Get language dict with fallback to English for missing keys
    lang_dict = RECOMMENDATIONS_TRANSLATIONS.get(lang, {})
    t = lambda key: lang_dict.get(key, RECOMMENDATIONS_TRANSLATIONS['en'].get(key, key))
    
    recommendations = {
        'title': t('breathing_health'),
        'status': status,
        'exercises': [],
        'lifestyle': [],
        'tips': []
    }
    
    if status == 'Normal':
        recommendations['exercises'] = [
            t('deep_breathing_5_min'),
            t('continue_current_activity')
        ]
        recommendations['lifestyle'] = [
            t('good_air_quality'),
            t('stay_active_mobile')
        ]
        recommendations['tips'] = [
            t('breathing_pattern_healthy'),
            t('keep_practicing_breathing')
        ]
    
    elif status == 'Shallow Breathing':
        recommendations['exercises'] = [
            t('diaphragmatic_breathing'),
            t('box_breathing'),
            t('gentle_chest_expansion')
        ]
        recommendations['lifestyle'] = [
            t('good_posture_sitting'),
            t('breathing_breaks_hour'),
            t('avoid_restrictive')
        ]
        recommendations['tips'] = [
            t('shallow_breathing_detected'),
            t('lungs_hold_more_air')
        ]
    
    elif status == 'Irregular':
        recommendations['exercises'] = [
            t('paced_breathing'),
            t('relaxed_breathing_exercises'),
            t('gentle_yoga_breath')
        ]
        recommendations['lifestyle'] = [
            t('reduce_stress_possible'),
            t('practice_mindfulness'),
            t('monitor_breathing_patterns')
        ]
        recommendations['tips'] = [
            t('irregular_breathing_noticed'),
            t('regular_practice_improves')
        ]
    
    elif status == 'Apnea Risk':
        recommendations['exercises'] = [
            t('breathing_awareness'),
            t('gentle_aerobic_activity'),
            t('consult_sleep_specialist')
        ]
        recommendations['lifestyle'] = [
            t('sleep_on_side'),
            t('maintain_healthy_weight'),
            t('avoid_alcohol_bed')
        ]
        recommendations['tips'] = [
            t('potential_apnea_risk'),
            t('good_sleep_position')
        ]
    
    return recommendations

def get_speech_recommendations(prediction, lang='en'):
    """Get recommendations for speech patterns"""
    pattern = prediction['pattern']
    # Get language dict with fallback to English for missing keys
    lang_dict = RECOMMENDATIONS_TRANSLATIONS.get(lang, {})
    t = lambda key: lang_dict.get(key, RECOMMENDATIONS_TRANSLATIONS['en'].get(key, key))
    
    recommendations = {
        'title': t('speech_communication'),
        'status': pattern,
        'exercises': [],
        'lifestyle': [],
        'tips': []
    }
    
    if pattern == 'Normal Speech':
        recommendations['exercises'] = [
            t('continue_conversation'),
            t('reading_aloud_10')
        ]
        recommendations['lifestyle'] = [
            t('stay_socially_engaged'),
            t('maintain_communication')
        ]
        recommendations['tips'] = [
            t('speech_patterns_healthy'),
            t('keep_practicing_communication')
        ]
    
    elif pattern == 'Slurred/Slow':
        recommendations['exercises'] = [
            t('tongue_twisters_5'),
            t('exaggerate_mouth'),
            t('reading_slowly_clearly'),
            t('facial_muscle_exercises')
        ]
        recommendations['lifestyle'] = [
            t('speak_slowly_deliberately'),
            t('take_pauses_sentences'),
            t('stay_hydrated')
        ]
        recommendations['tips'] = [
            t('speech_clarity_exercises'),
            t('practice_makes_perfect')
        ]
    
    elif pattern == 'Stressed Speech':
        recommendations['exercises'] = [
            t('breathing_before_speaking'),
            t('speak_slower_pace'),
            t('relaxation_techniques'),
            t('mindful_communication')
        ]
        recommendations['lifestyle'] = [
            t('take_breaks_conversations'),
            t('practice_stress_management'),
            t('ensure_adequate_rest')
        ]
        recommendations['tips'] = [
            t('stress_affects_speech'),
            t('deep_breaths_speaking')
        ]
    
    return recommendations

def get_emotion_recommendations(prediction, lang='en'):
    """Get recommendations for emotional wellbeing"""
    state = prediction['state']
    # Get language dict with fallback to English for missing keys
    lang_dict = RECOMMENDATIONS_TRANSLATIONS.get(lang, {})
    t = lambda key: lang_dict.get(key, RECOMMENDATIONS_TRANSLATIONS['en'].get(key, key))
    
    recommendations = {
        'title': t('emotional_wellbeing'),
        'status': state,
        'exercises': [],
        'lifestyle': [],
        'tips': []
    }
    
    if state == 'Happy':
        recommendations['exercises'] = [
            t('engage_enjoyable_activities'),
            t('physical_exercise_mood')
        ]
        recommendations['lifestyle'] = [
            t('maintain_communication'),
            t('spend_time_hobbies')
        ]
        recommendations['tips'] = [
            t('wonderful_emotional'),
            t('positive_energy_valuable')
        ]
    
    elif state == 'Neutral':
        recommendations['exercises'] = [
            t('engage_enjoyable_activities'),
            t('try_something_new'),
            t('physical_exercise_mood')
        ]
        recommendations['lifestyle'] = [
            t('connect_friends_family'),
            t('practice_gratitude_daily'),
            t('spend_time_hobbies')
        ]
        recommendations['tips'] = [
            t('neutral_state_normal'),
            t('small_activities_boost')
        ]
    
    elif state == 'Stressed':
        recommendations['exercises'] = [
            t('deep_breathing_10'),
            t('progressive_muscle'),
            t('gentle_yoga_breath'),
            t('nature_walks')
        ]
        recommendations['lifestyle'] = [
            t('prioritize_sleep_7_9'),
            t('limit_screen_time'),
            t('talk_someone_trust'),
            t('break_tasks_steps')
        ]
        recommendations['tips'] = [
            t('stress_manageable'),
            t('be_kind_yourself')
        ]
    
    elif state == 'Sad':
        recommendations['exercises'] = [
            t('light_physical_walks'),
            t('breathing_before_speaking'),
            t('creative_expression')
        ]
        recommendations['lifestyle'] = [
            t('reach_supportive'),
            t('maintain_routine'),
            t('speak_counselor'),
            t('achievable_tasks')
        ]
        recommendations['tips'] = [
            t('feelings_valid_temporary'),
            t('support_available')
        ]
    
    return recommendations

def get_posture_recommendations(prediction, lang='en'):
    """Get recommendations for posture improvement"""
    posture_type = prediction['posture']
    score = prediction['score']
    # Get language dict with fallback to English for missing keys
    lang_dict = RECOMMENDATIONS_TRANSLATIONS.get(lang, {})
    t = lambda key: lang_dict.get(key, RECOMMENDATIONS_TRANSLATIONS['en'].get(key, key))
    
    recommendations = {
        'title': t('posture_health'),
        'status': f'{posture_type} (Score: {score:.0f}/100)',
        'exercises': [],
        'lifestyle': [],
        'tips': []
    }
    
    if posture_type == 'Good Posture':
        recommendations['exercises'] = [
            t('core_strengthening'),
            t('maintain_flexibility')
        ]
        recommendations['lifestyle'] = [
            t('good_posture_habits'),
            t('movement_breaks')
        ]
        recommendations['tips'] = [
            t('excellent_posture'),
            t('maintaining_prevents')
        ]
    
    elif posture_type == 'Forward Head Posture':
        recommendations['exercises'] = [
            t('chin_tucks_10'),
            t('neck_stretches'),
            t('upper_back_strengthening'),
            t('chest_stretches_30')
        ]
        recommendations['lifestyle'] = [
            t('adjust_screen_height'),
            t('ergonomic_workspace'),
            t('posture_check_reminders'),
            t('avoid_prolonged_phone')
        ]
        recommendations['tips'] = [
            t('forward_very_common'),
            t('small_adjustments_big')
        ]
    
    elif posture_type == 'Slouched Sitting':
        recommendations['exercises'] = [
            t('core_exercises_planks'),
            t('back_extensions_superman'),
            t('hip_flexor_stretches'),
            t('shoulder_blade_squeezes')
        ]
        recommendations['lifestyle'] = [
            t('use_lumbar_support'),
            t('stand_up_30_minutes'),
            t('adjust_chair_height'),
            t('sit_tall_shoulders')
        ]
        recommendations['tips'] = [
            t('slouching_stress_spine'),
            t('building_core_strength')
        ]
    
    return recommendations

def get_all_recommendations(predictions, lang='en'):
    """Get recommendations for all prediction results"""
    recommendations = {}
    
    if 'heartbeat' in predictions:
        recommendations['heartbeat'] = get_heartbeat_recommendations(predictions['heartbeat'], lang)
    
    if 'glucose' in predictions:
        recommendations['glucose'] = get_glucose_recommendations(predictions['glucose'], lang)
    
    if 'breathing' in predictions:
        recommendations['breathing'] = get_breathing_recommendations(predictions['breathing'], lang)
    
    if 'speech' in predictions:
        recommendations['speech'] = get_speech_recommendations(predictions['speech'], lang)
    
    if 'emotion' in predictions:
        recommendations['emotion'] = get_emotion_recommendations(predictions['emotion'], lang)
    
    if 'posture' in predictions:
        recommendations['posture'] = get_posture_recommendations(predictions['posture'], lang)
    
    return recommendations

def get_summary_message(predictions, lang='en'):
    """Generate overall health summary message"""
    # Get language dict with fallback to English for missing keys
    lang_dict = RECOMMENDATIONS_TRANSLATIONS.get(lang, {})
    t = lambda key: lang_dict.get(key, RECOMMENDATIONS_TRANSLATIONS['en'].get(key, key))
    issues = []
    strengths = []
    
    # Check each prediction
    if 'heartbeat' in predictions:
        if predictions['heartbeat']['status'] != 'Normal':
            issues.append('heart rhythm')
        else:
            strengths.append('heart health')
    
    if 'glucose' in predictions:
        if predictions['glucose']['range'] != 'Normal':
            issues.append('blood glucose')
        else:
            strengths.append('glucose control')
    
    if 'breathing' in predictions:
        if predictions['breathing']['status'] != 'Normal':
            issues.append('breathing pattern')
        else:
            strengths.append('breathing')
    
    if 'speech' in predictions:
        if predictions['speech']['pattern'] != 'Normal Speech':
            issues.append('speech clarity')
        else:
            strengths.append('communication')
    
    if 'emotion' in predictions:
        if predictions['emotion']['state'] in ['Stressed', 'Sad']:
            issues.append('emotional wellbeing')
        else:
            strengths.append('emotional state')
    
    if 'posture' in predictions:
        if predictions['posture']['posture'] != 'Good Posture':
            issues.append('posture')
        else:
            strengths.append('posture')
    
    # Generate message based on language
    message = ""
    
    if strengths:
        strengths_str = ', '.join(strengths)
        message += f"{t('great_job_maintaining')} {strengths_str}! "
    
    if issues:
        issues_str = ', '.join(issues)
        message += f"{t('focus_areas_improvement')}: {issues_str}. {t('follow_recommendations')}"
    elif not strengths:
        message += t('keep_up_rehabilitation')
    else:
        message += t('continue_healthy_stay')
    
    return message