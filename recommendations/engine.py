"""
Recommendation Engine
Provides personalized rehabilitation recommendations based on AI predictions
"""

def get_heartbeat_recommendations(prediction):
    """Get recommendations for heartbeat abnormalities"""
    status = prediction['status']
    
    recommendations = {
        'title': 'Heart Health',
        'status': status,
        'exercises': [],
        'lifestyle': [],
        'tips': []
    }
    
    if status == 'Normal':
        recommendations['exercises'] = [
            'Continue moderate aerobic exercise (20-30 min, 3-4 times/week)',
            'Walking, swimming, or cycling at comfortable pace'
        ]
        recommendations['lifestyle'] = [
            'Maintain current healthy habits',
            'Stay hydrated throughout the day'
        ]
        recommendations['tips'] = [
            'Your heart rhythm is healthy!',
            'Keep up the good work with regular activity'
        ]
    
    elif status == 'Bradycardia':
        recommendations['exercises'] = [
            'Light aerobic activities to gradually increase heart rate',
            'Gentle walking for 15-20 minutes daily',
            'Stretching and flexibility exercises'
        ]
        recommendations['lifestyle'] = [
            'Avoid sudden intense activities',
            'Stay warm and comfortable',
            'Monitor how you feel during activities'
        ]
        recommendations['tips'] = [
            'Slow heart rate detected - speak with your healthcare provider',
            'Gradual increase in activity is key'
        ]
    
    elif status == 'Tachycardia':
        recommendations['exercises'] = [
            'Gentle breathing exercises',
            'Slow-paced yoga or tai chi',
            'Avoid high-intensity workouts temporarily'
        ]
        recommendations['lifestyle'] = [
            'Reduce caffeine intake',
            'Practice stress management',
            'Ensure adequate rest and sleep'
        ]
        recommendations['tips'] = [
            'Elevated heart rate detected',
            'Focus on relaxation and calm activities'
        ]
    
    elif status == 'Irregular':
        recommendations['exercises'] = [
            'Low-impact activities under supervision',
            'Seated exercises and gentle movements',
            'Avoid strenuous activities'
        ]
        recommendations['lifestyle'] = [
            'Monitor heart rate regularly',
            'Consult healthcare provider',
            'Keep a symptom diary'
        ]
        recommendations['tips'] = [
            'Irregular rhythm detected - medical consultation recommended',
            'Gentle activity is safest for now'
        ]
    
    return recommendations

def get_glucose_recommendations(prediction):
    """Get recommendations for glucose management"""
    range_label = prediction['range']
    
    recommendations = {
        'title': 'Blood Glucose',
        'status': range_label,
        'exercises': [],
        'lifestyle': [],
        'tips': []
    }
    
    if range_label == 'Normal':
        recommendations['exercises'] = [
            'Regular physical activity (30 min, 5 days/week)',
            'Mix of cardio and strength training'
        ]
        recommendations['lifestyle'] = [
            'Maintain balanced meals',
            'Continue healthy eating habits'
        ]
        recommendations['tips'] = [
            'Glucose levels are well-controlled!',
            'Keep monitoring and staying active'
        ]
    
    elif range_label == 'Low':
        recommendations['exercises'] = [
            'Light activity after meals',
            'Avoid exercising on empty stomach'
        ]
        recommendations['lifestyle'] = [
            'Eat small, frequent meals',
            'Keep healthy snacks available',
            'Monitor blood sugar before activities'
        ]
        recommendations['tips'] = [
            'Low glucose detected - ensure regular meals',
            'Carry quick-acting carbohydrates'
        ]
    
    elif range_label == 'High':
        recommendations['exercises'] = [
            'Post-meal walking (15-20 minutes)',
            'Regular moderate exercise',
            'Strength training 2-3 times per week'
        ]
        recommendations['lifestyle'] = [
            'Focus on whole foods and vegetables',
            'Limit refined carbohydrates',
            'Stay well-hydrated'
        ]
        recommendations['tips'] = [
            'Elevated glucose detected',
            'Physical activity helps regulate blood sugar'
        ]
    
    return recommendations

def get_breathing_recommendations(prediction):
    """Get recommendations for breathing patterns"""
    status = prediction['status']
    
    recommendations = {
        'title': 'Breathing Health',
        'status': status,
        'exercises': [],
        'lifestyle': [],
        'tips': []
    }
    
    if status == 'Normal':
        recommendations['exercises'] = [
            'Deep breathing exercises (5 min daily)',
            'Continue current activity level'
        ]
        recommendations['lifestyle'] = [
            'Maintain good air quality in living spaces',
            'Stay active and mobile'
        ]
        recommendations['tips'] = [
            'Breathing pattern is healthy!',
            'Keep practicing good breathing habits'
        ]
    
    elif status == 'Shallow Breathing':
        recommendations['exercises'] = [
            'Diaphragmatic breathing: Breathe deeply into belly (5-10 min, 3x/day)',
            'Box breathing: Inhale 4s, hold 4s, exhale 4s, hold 4s',
            'Gentle chest expansion exercises'
        ]
        recommendations['lifestyle'] = [
            'Practice good posture while sitting',
            'Take breathing breaks every hour',
            'Avoid restrictive clothing'
        ]
        recommendations['tips'] = [
            'Shallow breathing detected - focus on deep breaths',
            'Your lungs can hold more air with practice'
        ]
    
    elif status == 'Irregular':
        recommendations['exercises'] = [
            'Paced breathing: Count to 4 on inhale, 6 on exhale',
            'Relaxed breathing exercises',
            'Gentle yoga focusing on breath'
        ]
        recommendations['lifestyle'] = [
            'Reduce stress where possible',
            'Practice mindfulness',
            'Monitor breathing patterns'
        ]
        recommendations['tips'] = [
            'Irregular breathing pattern noticed',
            'Regular practice improves breathing rhythm'
        ]
    
    elif status == 'Apnea Risk':
        recommendations['exercises'] = [
            'Breathing awareness exercises',
            'Gentle aerobic activity',
            'Consult sleep specialist'
        ]
        recommendations['lifestyle'] = [
            'Sleep on your side',
            'Maintain healthy weight',
            'Avoid alcohol before bed'
        ]
        recommendations['tips'] = [
            'Potential apnea risk - medical evaluation recommended',
            'Good sleep position helps breathing'
        ]
    
    return recommendations

def get_speech_recommendations(prediction):
    """Get recommendations for speech patterns"""
    pattern = prediction['pattern']
    
    recommendations = {
        'title': 'Speech & Communication',
        'status': pattern,
        'exercises': [],
        'lifestyle': [],
        'tips': []
    }
    
    if pattern == 'Normal Speech':
        recommendations['exercises'] = [
            'Continue regular conversation practice',
            'Reading aloud for 10 minutes daily'
        ]
        recommendations['lifestyle'] = [
            'Stay socially engaged',
            'Maintain communication habits'
        ]
        recommendations['tips'] = [
            'Speech patterns are healthy!',
            'Keep practicing regular communication'
        ]
    
    elif pattern == 'Slurred/Slow':
        recommendations['exercises'] = [
            'Tongue twisters practice (5 min daily)',
            'Exaggerate mouth movements when speaking',
            'Reading aloud slowly and clearly',
            'Facial muscle exercises'
        ]
        recommendations['lifestyle'] = [
            'Speak slowly and deliberately',
            'Take pauses between sentences',
            'Stay well-hydrated'
        ]
        recommendations['tips'] = [
            'Speech clarity exercises will help',
            'Practice makes perfect - be patient with yourself'
        ]
    
    elif pattern == 'Stressed Speech':
        recommendations['exercises'] = [
            'Breathing exercises before speaking',
            'Practice speaking at slower pace',
            'Relaxation techniques',
            'Mindful communication practice'
        ]
        recommendations['lifestyle'] = [
            'Take breaks during conversations',
            'Practice stress management',
            'Get adequate rest'
        ]
        recommendations['tips'] = [
            'Stress affects speech - relaxation helps',
            'Deep breaths before speaking can help'
        ]
    
    return recommendations

def get_emotion_recommendations(prediction):
    """Get recommendations for emotional wellbeing"""
    state = prediction['state']
    
    recommendations = {
        'title': 'Emotional Wellbeing',
        'status': state,
        'exercises': [],
        'lifestyle': [],
        'tips': []
    }
    
    if state == 'Happy':
        recommendations['exercises'] = [
            'Continue activities that bring joy',
            'Share positivity with others'
        ]
        recommendations['lifestyle'] = [
            'Maintain social connections',
            'Keep up healthy routines'
        ]
        recommendations['tips'] = [
            'Wonderful emotional state!',
            'Your positive energy is valuable'
        ]
    
    elif state == 'Neutral':
        recommendations['exercises'] = [
            'Engage in enjoyable activities',
            'Try something new this week',
            'Physical exercise (boosts mood)'
        ]
        recommendations['lifestyle'] = [
            'Connect with friends or family',
            'Practice gratitude daily',
            'Spend time on hobbies'
        ]
        recommendations['tips'] = [
            'Neutral state is normal',
            'Small activities can boost your mood'
        ]
    
    elif state == 'Stressed':
        recommendations['exercises'] = [
            'Deep breathing exercises (10 min, 2-3x/day)',
            'Progressive muscle relaxation',
            'Gentle yoga or stretching',
            'Nature walks'
        ]
        recommendations['lifestyle'] = [
            'Prioritize sleep (7-9 hours)',
            'Limit screen time before bed',
            'Talk to someone you trust',
            'Break tasks into smaller steps'
        ]
        recommendations['tips'] = [
            'Stress is manageable with the right tools',
            'Be kind to yourself during difficult times'
        ]
    
    elif state == 'Sad':
        recommendations['exercises'] = [
            'Light physical activity (walks, gentle exercise)',
            'Breathing and mindfulness exercises',
            'Creative expression (art, music, writing)'
        ]
        recommendations['lifestyle'] = [
            'Reach out to supportive people',
            'Maintain routine where possible',
            'Consider speaking with a counselor',
            'Engage in small, achievable tasks'
        ]
        recommendations['tips'] = [
            'These feelings are valid and temporary',
            'Support is available - you don\'t have to go through this alone'
        ]
    
    return recommendations

def get_posture_recommendations(prediction):
    """Get recommendations for posture improvement"""
    posture_type = prediction['posture']
    score = prediction['score']
    
    recommendations = {
        'title': 'Posture Health',
        'status': f'{posture_type} (Score: {score:.0f}/100)',
        'exercises': [],
        'lifestyle': [],
        'tips': []
    }
    
    if posture_type == 'Good Posture':
        recommendations['exercises'] = [
            'Continue core strengthening exercises',
            'Maintain flexibility with stretching'
        ]
        recommendations['lifestyle'] = [
            'Keep practicing good posture habits',
            'Take movement breaks regularly'
        ]
        recommendations['tips'] = [
            'Excellent posture!',
            'Maintaining good posture prevents future issues'
        ]
    
    elif posture_type == 'Forward Head Posture':
        recommendations['exercises'] = [
            'Chin tucks: Pull chin back (10 reps, 3x/day)',
            'Neck stretches: Gentle side-to-side and up-down',
            'Upper back strengthening: Rows and reverse flies',
            'Chest stretches: Doorway stretch (30s, 3 reps)'
        ]
        recommendations['lifestyle'] = [
            'Adjust screen height to eye level',
            'Use ergonomic workspace setup',
            'Set posture check reminders',
            'Avoid prolonged phone use'
        ]
        recommendations['tips'] = [
            'Forward head posture is very common with screen use',
            'Small adjustments make big differences'
        ]
    
    elif posture_type == 'Slouched Sitting':
        recommendations['exercises'] = [
            'Core exercises: Planks, bridges (daily)',
            'Back extensions: Superman pose (10 reps, 2 sets)',
            'Hip flexor stretches (30s each side)',
            'Shoulder blade squeezes (15 reps, 3x/day)'
        ]
        recommendations['lifestyle'] = [
            'Use lumbar support when sitting',
            'Stand up every 30 minutes',
            'Adjust chair height properly',
            'Practice sitting tall with shoulders back'
        ]
        recommendations['tips'] = [
            'Slouching puts stress on your spine',
            'Building core strength helps maintain posture'
        ]
    
    return recommendations

def get_all_recommendations(predictions):
    """Get recommendations for all prediction results"""
    recommendations = {}
    
    if 'heartbeat' in predictions:
        recommendations['heartbeat'] = get_heartbeat_recommendations(predictions['heartbeat'])
    
    if 'glucose' in predictions:
        recommendations['glucose'] = get_glucose_recommendations(predictions['glucose'])
    
    if 'breathing' in predictions:
        recommendations['breathing'] = get_breathing_recommendations(predictions['breathing'])
    
    if 'speech' in predictions:
        recommendations['speech'] = get_speech_recommendations(predictions['speech'])
    
    if 'emotion' in predictions:
        recommendations['emotion'] = get_emotion_recommendations(predictions['emotion'])
    
    if 'posture' in predictions:
        recommendations['posture'] = get_posture_recommendations(predictions['posture'])
    
    return recommendations

def get_summary_message(predictions):
    """Generate overall health summary message"""
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
    
    # Generate message
    message = ""
    
    if strengths:
        message += f"Great job maintaining {', '.join(strengths)}! "
    
    if issues:
        message += f"Focus areas for improvement: {', '.join(issues)}. "
        message += "Follow the recommendations below to support your rehabilitation journey."
    elif not strengths:
        message += "Keep up your rehabilitation activities and monitor your progress."
    else:
        message += "Continue your healthy habits and stay consistent with your routine."
    
    return message