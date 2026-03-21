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
        # Section headings
        'exercises_activities': 'Exercises & Activities',
        'lifestyle_tips': 'Lifestyle Tips',
        'important_notes': 'Important Notes',
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
        'exercises_activities': 'व्यायाम और गतिविधियां',
        'lifestyle_tips': 'जीवनशैली के सुझाव',
        'important_notes': 'महत्वपूर्ण नोट्स',
        'continue_moderate_aerobic': 'मध्यम हृदय व्यायाम (20-30 मिनट, सप्ताह में 3-4 बार) जारी रखें',
        'walking_swimming_cycling': 'आरामदायक गति से चलना, तैराकी या साइकिल चलाना',
        'maintain_current_healthy': 'अपनी वर्तमान स्वस्थ आदतें बनाए रखें',
        'stay_hydrated': 'दिनभर हाइड्रेटेड रहें',
        'heart_rhythm_healthy': 'आपकी हृदय गति स्वस्थ है!',
        'keep_up_good_work': 'नियमित गतिविधि के साथ अच्छा काम करते रहें',
        'light_aerobic_activities': 'हल्की एरोबिक गतिविधियां हृदय गति को धीरे-धीरे बढ़ाने के लिए',
        'gentle_walking_15_20': 'प्रतिदिन 15-20 मिनट की कोमल सैर',
        'stretching_flexibility': 'स्ट्रेचिंग और लचीलापन व्यायाम',
        'avoid_sudden_intense': 'अचानक तीव्र गतिविधियों से बचें',
        'stay_warm_comfortable': 'गर्म और आरामदायक रहें',
        'monitor_feel_activities': 'गतिविधियों के दौरान महसूस करें कि आप कैसा महसूस कर रहे हैं',
        'slow_heart_rate_detected': 'धीमी हृदय गति का पता चला - अपने स्वास्थ्यसेवा प्रदाता से बात करें',
        'gradual_increase_activity': 'गतिविधि में क्रमिक वृद्धि मुख्य है',
        'gentle_breathing_exercises': 'कोमल श्वास व्यायाम',
        'slow_paced_yoga_tai_chi': 'धीमी गति से योग या ताई ची',
        'avoid_high_intensity': 'उच्च-तीव्रता व्यायामों से अस्थायी रूप से बचें',
        'reduce_caffeine_intake': 'कैफीन का सेवन कम करें',
        'practice_stress_management': 'तनाव प्रबंधन का अभ्यास करें',
        'ensure_adequate_rest': 'पर्याप्त आराम और नींद सुनिश्चित करें',
        'elevated_heart_rate': 'बढ़ी हुई हृदय गति का पता चला',
        'focus_relaxation_calm': 'विश्राम और शांत गतिविधियों पर ध्यान दें',
        'low_impact_activities': 'कम प्रभाव वाली गतिविधियां पर्यवेक्षण के अंतर्गत',
        'seated_exercises_gentle': 'बैठी हुई व्यायाम और कोमल आंदोलन',
        'avoid_strenuous': 'मेहनती गतिविधियों से बचें',
        'monitor_heart_rate': 'नियमित रूप से हृदय गति की निगरानी करें',
        'consult_healthcare': 'स्वास्थ्यसेवा प्रदाता से परामर्श लें',
        'keep_symptom_diary': 'एक लक्षण डायरी रखें',
        'irregular_rhythm_detected': 'अनियमित ताल का पता चला - चिकित्सा परामर्श की सिफारिश की जाती है',
        'gentle_activity_safest': 'इस समय कोमल गतिविधि सबसे सुरक्षित है',
        'regular_physical_activity': 'नियमित शारीरिक गतिविधि (30 मिनट, सप्ताह में 5 दिन)',
        'mix_cardio_strength': 'कार्डियो और शक्ति प्रशिक्षण का मिश्रण',
        'maintain_balanced_meals': 'संतुलित भोजन बनाए रखें',
        'continue_healthy_eating': 'स्वस्थ खाने की आदतें जारी रखें',
        'glucose_well_controlled': 'ग्लूकोज का स्तर अच्छी तरह नियंत्रित है!',
        'keep_monitoring_active': 'निगरानी जारी रखें और सक्रिय रहें',
        'light_activity_after': 'भोजन के बाद हल्की गतिविधि',
        'avoid_empty_stomach': 'खाली पेट व्यायाम से बचें',
        'eat_small_frequent': 'छोटे, बार-बार भोजन करें',
        'keep_healthy_snacks': 'स्वस्थ स्नैक्स को हाथ में रखें',
        'monitor_blood_sugar': 'गतिविधियों से पहले रक्त शर्करा की निगरानी करें',
        'low_glucose_detected': 'कम ग्लूकोज का पता चला - नियमित भोजन सुनिश्चित करें',
        'carry_quick_carbs': 'तेजी से अभिनय करने वाले कार्बोहाइड्रेट ले जाएं',
        'post_meal_walking': 'भोजन के बाद सैर (15-20 मिनट)',
        'strength_training_2_3': 'शक्ति प्रशिक्षण सप्ताह में 2-3 बार',
        'focus_whole_foods': 'पूरे खाद्य पदार्थ और सब्जियों पर ध्यान दें',
        'limit_refined_carbs': 'परिष्कृत कार्बोहाइड्रेट को सीमित करें',
        'stay_well_hydrated': 'अच्छी तरह से जलयुक्त रहें',
        'elevated_glucose': 'बढ़ा हुआ ग्लूकोज का पता चला',
        'physical_activity_helps': 'शारीरिक गतिविधि रक्त शर्करा को नियंत्रित करने में सहायता करती है',
        'deep_breathing_5_min': 'गहरी श्वास व्यायाम (प्रतिदिन 5 मिनट)',
        'continue_current_activity': 'वर्तमान गतिविधि स्तर जारी रखें',
        'good_air_quality': 'रहने की जगह में अच्छी वायु गुणवत्ता बनाए रखें',
        'stay_active_mobile': 'सक्रिय और मोबाइल रहें',
        'breathing_pattern_healthy': 'श्वास पैटर्न स्वस्थ है!',
        'keep_practicing_breathing': 'अच्छे श्वास की आदतों का अभ्यास जारी रखें',
        'diaphragmatic_breathing': 'डायाफ्रामिक श्वास: पेट में गहरी सांस लें (5-10 मिनट, प्रतिदिन 3 बार)',
        'box_breathing': 'बॉक्स श्वास: 4 सेकंड के लिए सांस लें, 4 सेकंड रोकें, 4 सेकंड बाहर निकालें, 4 सेकंड रोकें',
        'gentle_chest_expansion': 'कोमल छाती विस्तार व्यायाम',
        'good_posture_sitting': 'बैठते समय अच्छी मुद्रा का अभ्यास करें',
        'breathing_breaks_hour': 'हर घंटे श्वास विराम लें',
        'avoid_restrictive': 'प्रतिबंधक कपड़ों से बचें',
        'shallow_breathing_detected': 'उथली श्वास का पता चला - गहरी सांसों पर ध्यान दें',
        'lungs_hold_more_air': 'आपके फेफड़े अभ्यास के साथ अधिक हवा रख सकते हैं',
        'paced_breathing': 'गति की श्वास: साँस लेते समय 4 तक गिनें, साँस छोड़ते समय 6 तक',
        'relaxed_breathing_exercises': 'आरामदायक श्वास व्यायाम',
        'gentle_yoga_breath': 'श्वास पर ध्यान केंद्रित करते हुए कोमल योग',
        'reduce_stress_possible': 'कहीं भी संभव हो तनाव कम करें',
        'practice_mindfulness': 'माइंडफुलनेस का अभ्यास करें',
        'monitor_breathing_patterns': 'श्वास पैटर्न की निगरानी करें',
        'irregular_breathing_noticed': 'अनियमित श्वास पैटर्न देखा गया',
        'regular_practice_improves': 'नियमित अभ्यास श्वास की लय में सुधार करता है',
        'breathing_awareness': 'श्वास जागरूकता व्यायाम',
        'gentle_aerobic_activity': 'कोमल एरोबिक गतिविधि',
        'consult_sleep_specialist': 'नींद विशेषज्ञ से परामर्श लें',
        'sleep_on_side': 'अपने पक्ष पर सोएं',
        'maintain_healthy_weight': 'स्वस्थ वजन बनाए रखें',
        'avoid_alcohol_bed': 'सोने से पहले शराब से बचें',
        'potential_apnea_risk': 'संभावित अप्निया जोखिम - चिकित्सा मूल्यांकन की सिफारिश की जाती है',
        'good_sleep_position': 'अच्छी नींद की मुद्रा श्वास में मदद करती है',
        'continue_conversation': 'नियमित बातचीत का अभ्यास जारी रखें',
        'reading_aloud_10': 'प्रतिदिन 10 मिनट के लिए जोर से पढ़ना',
        'stay_socially_engaged': 'सामाजिक रूप से जुड़े रहें',
        'maintain_communication': 'संचार की आदतें बनाए रखें',
        'speech_patterns_healthy': 'भाषण के पैटर्न स्वस्थ हैं!',
        'keep_practicing_communication': 'नियमित संचार का अभ्यास जारी रखें',
        'tongue_twisters_5': 'जीभ के मोड़ का अभ्यास (प्रतिदिन 5 मिनट)',
        'exaggerate_mouth': 'बोलते समय मुंह की गतिविधियों को अतिरंजित करें',
        'reading_slowly_clearly': 'धीरे और स्पष्ट रूप से जोर से पढ़ना',
        'facial_muscle_exercises': 'चेहरे की मांसपेशी व्यायाम',
        'speak_slowly_deliberately': 'धीरे और जानबूझकर बोलें',
        'take_pauses_sentences': 'वाक्यों के बीच विराम लें',
        'speech_clarity_exercises': 'भाषण स्पष्टता व्यायाम सहायक होगा',
        'practice_makes_perfect': 'अभ्यास सही बनाता है - अपने साथ धैर्य रखें',
        'breathing_before_speaking': 'बोलने से पहले श्वास व्यायाम',
        'speak_slower_pace': 'अधीन गति से बोलने का अभ्यास करें',
        'relaxation_techniques': 'विश्राम तकनीकें',
        'mindful_communication': 'सचेत संचार अभ्यास',
        'take_breaks_conversations': 'बातचीत के दौरान विराम लें',
        'stress_affects_speech': 'तनाव भाषण को प्रभावित करता है - विश्राम सहायक है',
        'deep_breaths_speaking': 'बोलने से पहले गहरी सांसें लेना मदद कर सकता है',
        'wonderful_emotional': 'शानदार भावनात्मक स्थिति!',
        'positive_energy_valuable': 'आपकी सकारात्मक ऊर्जा मूल्यवान है',
        'engage_enjoyable_activities': 'आनंददायक गतिविधियों में संलग्न हों',
        'try_something_new': 'इस सप्ताह कुछ नया आजमाएं',
        'physical_exercise_mood': 'शारीरिक व्यायाम (मनोदशा को बढ़ाता है)',
        'connect_friends_family': 'दोस्तों या परिवार के साथ जुड़ें',
        'practice_gratitude_daily': 'प्रतिदिन कृतज्ञता का अभ्यास करें',
        'spend_time_hobbies': 'शौक पर समय बिताएं',
        'neutral_state_normal': 'तटस्थ अवस्था सामान्य है',
        'small_activities_boost': 'छोटी गतिविधियां आपके मूड को बढ़ा सकती हैं',
        'deep_breathing_10': 'गहरी श्वास व्यायाम (10 मिनट, प्रतिदिन 2-3 बार)',
        'progressive_muscle': 'प्रगतिशील मांसपेशी छूट',
        'nature_walks': 'प्रकृति में सैर',
        'prioritize_sleep_7_9': 'नींद को प्राथमिकता दें (7-9 घंटे)',
        'limit_screen_time': 'सोने से पहले स्क्रीन समय सीमित करें',
        'talk_someone_trust': 'किसी विश्वसनीय व्यक्ति से बात करें',
        'break_tasks_steps': 'कार्यों को छोटे चरणों में विभाजित करें',
        'stress_manageable': 'सही उपकरणों के साथ तनाव प्रबंधनीय है',
        'be_kind_yourself': 'कठिन समय में अपने साथ दयालु रहें',
        'light_physical_walks': 'हल्की शारीरिक गतिविधि (सैर, कोमल व्यायाम)',
        'creative_expression': 'रचनात्मक अभिव्यक्ति (कला, संगीत, लेखन)',
        'reach_supportive': 'सहायक लोगों तक पहुँचें',
        'maintain_routine': 'जहाँ संभव हो दिनचर्या बनाए रखें',
        'speak_counselor': 'एक सलाहकार से बात करने पर विचार करें',
        'achievable_tasks': 'छोटी, प्राप्य गतिविधियों में संलग्न हों',
        'feelings_valid_temporary': 'ये भावनाएं वैध और अस्थायी हैं',
        'support_available': 'समर्थन उपलब्ध है - आपको इससे अकेले गुजरना नहीं है',
        'core_strengthening': 'मूल शक्तिशाली करने व्यायाम जारी रखें',
        'maintain_flexibility': 'स्ट्रेचिंग के साथ लचीलापन बनाए रखें',
        'good_posture_habits': 'अच्छी मुद्रा की आदतों का अभ्यास जारी रखें',
        'movement_breaks': 'नियमित रूप से आंदोलन विराम लें',
        'excellent_posture': 'उत्कृष्ट मुद्रा!',
        'maintaining_prevents': 'अच्छी मुद्रा बनाए रखना भविष्य की समस्याओं को रोकता है',
        'chin_tucks_10': 'ठुड्डी को खींचना: ठुड्डी को वापस खींचें (10 दोहराव, प्रतिदिन 3 बार)',
        'neck_stretches': 'गर्दन में खिंचाव: कोमल पक्ष से पक्ष और ऊपर नीचे',
        'upper_back_strengthening': 'ऊपरी पीठ को मजबूत करना: पंक्तियां और उल्टे उड़ता है',
        'chest_stretches_30': 'छाती में खिंचाव: दरवाजे का खिंचाव (30 सेकंड, 3 दोहराव)',
        'adjust_screen_height': 'स्क्रीन की ऊंचाई को आंखों के स्तर पर समायोजित करें',
        'ergonomic_workspace': 'एर्गोनोमिक वर्कस्पेस सेटअप का उपयोग करें',
        'posture_check_reminders': 'मुद्रा जांच अनुस्मारक सेट करें',
        'avoid_prolonged_phone': 'फोन के लंबे उपयोग से बचें',
        'forward_very_common': 'आगे की ओर सिर की मुद्रा स्क्रीन के उपयोग के साथ बहुत आम है',
        'small_adjustments_big': 'छोटे समायोजन बड़ा फर्क लाते हैं',
        'core_exercises_planks': 'मूल व्यायाम: पटनोज, पुल (दैनिक)',
        'back_extensions_superman': 'पीठ विस्तार: सुपरमैन पोज़ (10 दोहराव, 2 सेट)',
        'hip_flexor_stretches': 'हिप खिंचाव (30 सेकंड प्रत्येक पक्ष)',
        'shoulder_blade_squeezes': 'कंधे के ब्लेड को निचोड़ना (15 दोहराव, प्रतिदिन 3 बार)',
        'use_lumbar_support': 'बैठते समय काठी सहायता का उपयोग करें',
        'stand_up_30_minutes': 'हर 30 मिनट में खड़े हों',
        'adjust_chair_height': 'कुर्सी की ऊंचाई को ठीक से समायोजित करें',
        'sit_tall_shoulders': 'कंधों के साथ लंबा बैठने का अभ्यास करें',
        'slouching_stress_spine': 'झुकना आपकी रीढ़ पर दबाव डालता है',
        'building_core_strength': 'मूल शक्ति निर्माण मुद्रा को बनाए रखने में सहायता करता है',
        'great_job_maintaining': 'आपके द्वारा बनाए रखे गए की अच्छी काम',
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
        'exercises_activities': 'Ejercicios y Actividades',
        'lifestyle_tips': 'Consejos de Estilo de Vida',
        'important_notes': 'Notas Importantes',
        'continue_moderate_aerobic': 'Continúa con ejercicio aeróbico moderado (20-30 min, 3-4 veces/semana)',
        'walking_swimming_cycling': 'Caminar, nadar o andar en bicicleta a ritmo cómodo',
        'maintain_current_healthy': 'Mantén tus hábitos saludables actuales',
        'stay_hydrated': 'Mantente hidratado durante todo el día',
        'heart_rhythm_healthy': '¡Tu ritmo cardíaco es saludable!',
        'keep_up_good_work': 'Continúa con el buen trabajo con la actividad regular',
        'light_aerobic_activities': 'Actividades aeróbicas ligeras para aumentar gradualmente la frecuencia cardíaca',
        'gentle_walking_15_20': 'Caminar suavemente durante 15-20 minutos diarios',
        'stretching_flexibility': 'Ejercicios de estiramiento y flexibilidad',
        'avoid_sudden_intense': 'Evita actividades intensas repentinas',
        'stay_warm_comfortable': 'Mantente caliente y cómodo',
        'monitor_feel_activities': 'Monitorea cómo te sientes durante las actividades',
        'slow_heart_rate_detected': 'Se detectó una frecuencia cardíaca lenta - habla con tu proveedor de salud',
        'gradual_increase_activity': 'El aumento gradual en la actividad es clave',
        'gentle_breathing_exercises': 'Ejercicios de respiración suave',
        'slow_paced_yoga_tai_chi': 'Yoga a ritmo lento o tai chi',
        'avoid_high_intensity': 'Evita los entrenamientos de alta intensidad temporalmente',
        'reduce_caffeine_intake': 'Reduce la ingesta de cafeína',
        'practice_stress_management': 'Practica la gestión del estrés',
        'ensure_adequate_rest': 'Asegura descanso y sueño adecuados',
        'elevated_heart_rate': 'Se detectó una frecuencia cardíaca elevada',
        'focus_relaxation_calm': 'Enfocate en la relajación y actividades tranquilas',
        'low_impact_activities': 'Actividades de bajo impacto bajo supervisión',
        'seated_exercises_gentle': 'Ejercicios sentado y movimientos suaves',
        'avoid_strenuous': 'Evita actividades agotadoras',
        'monitor_heart_rate': 'Monitorea tu frecuencia cardíaca regularmente',
        'consult_healthcare': 'Consulta con tu proveedor de salud',
        'keep_symptom_diary': 'Mantén un diario de síntomas',
        'irregular_rhythm_detected': 'Se detectó ritmo irregular - se recomienda consulta médica',
        'gentle_activity_safest': 'La actividad suave es la más segura por ahora',
        'regular_physical_activity': 'Actividad física regular (30 min, 5 días/semana)',
        'mix_cardio_strength': 'Mezcla de entrenamiento cardiovascular y de fuerza',
        'maintain_balanced_meals': 'Mantén comidas equilibradas',
        'continue_healthy_eating': 'Continúa con hábitos de alimentación saludable',
        'glucose_well_controlled': '¡Los niveles de glucosa están bien controlados!',
        'keep_monitoring_active': 'Continúa monitoreando y mantente activo',
        'light_activity_after': 'Actividad ligera después de las comidas',
        'avoid_empty_stomach': 'Evita ejercitarte con el estómago vacío',
        'eat_small_frequent': 'Come porciones pequeñas y frecuentes',
        'keep_healthy_snacks': 'Mantén snacks saludables disponibles',
        'monitor_blood_sugar': 'Monitorea el azúcar en sangre antes de actividades',
        'low_glucose_detected': 'Se detectó glucosa baja - asegura comidas regulares',
        'carry_quick_carbs': 'Lleva carbohidratos de acción rápida',
        'post_meal_walking': 'Caminar después de comer (15-20 minutos)',
        'strength_training_2_3': 'Entrenamiento de fuerza 2-3 veces por semana',
        'focus_whole_foods': 'Enfócate en alimentos integrales y verduras',
        'limit_refined_carbs': 'Limita los carbohidratos refinados',
        'stay_well_hydrated': 'Mantente bien hidratado',
        'elevated_glucose': 'Se detectó glucosa elevada',
        'physical_activity_helps': 'La actividad física ayuda a regular el azúcar en sangre',
        'deep_breathing_5_min': 'Ejercicios de respiración profunda (5 min diarios)',
        'continue_current_activity': 'Continúa con el nivel de actividad actual',
        'good_air_quality': 'Mantén buena calidad del aire en los espacios de vida',
        'stay_active_mobile': 'Mantente activo y móvil',
        'breathing_pattern_healthy': '¡El patrón de respiración es saludable!',
        'keep_practicing_breathing': 'Continúa practicando buenos hábitos de respiración',
        'diaphragmatic_breathing': 'Respiración diafragmática: Respira profundamente en el vientre (5-10 min, 3x/día)',
        'box_breathing': 'Respiración de caja: Inhala 4s, sostén 4s, exhala 4s, sostén 4s',
        'gentle_chest_expansion': 'Ejercicios suaves de expansión torácica',
        'good_posture_sitting': 'Practica buena postura al sentarte',
        'breathing_breaks_hour': 'Toma pausas de respiración cada hora',
        'avoid_restrictive': 'Evita ropa restrictiva',
        'shallow_breathing_detected': 'Se detectó respiración superficial - enfócate en respiraciones profundas',
        'lungs_hold_more_air': 'Tus pulmones pueden sostener más aire con práctica',
        'paced_breathing': 'Respiración ritmada: Cuenta hasta 4 al inhalar, 6 al exhalar',
        'relaxed_breathing_exercises': 'Ejercicios de respiración relajada',
        'gentle_yoga_breath': 'Yoga suave enfocado en la respiración',
        'reduce_stress_possible': 'Reduce el estrés donde sea posible',
        'practice_mindfulness': 'Practica atención plena',
        'monitor_breathing_patterns': 'Monitorea patrones de respiración',
        'irregular_breathing_noticed': 'Se notó patrón de respiración irregular',
        'regular_practice_improves': 'La práctica regular mejora el ritmo de respiración',
        'breathing_awareness': 'Ejercicios de conciencia de la respiración',
        'gentle_aerobic_activity': 'Actividad aeróbica suave',
        'consult_sleep_specialist': 'Consulta con un especialista del sueño',
        'sleep_on_side': 'Duerme de lado',
        'maintain_healthy_weight': 'Mantén un peso saludable',
        'avoid_alcohol_bed': 'Evita alcohol antes de acostarte',
        'potential_apnea_risk': 'Riesgo potencial de apnea - se recomienda evaluación médica',
        'good_sleep_position': 'La buena posición de sueño ayuda con la respiración',
        'continue_conversation': 'Continúa practicando conversación regular',
        'reading_aloud_10': 'Lee en voz alta durante 10 minutos diarios',
        'stay_socially_engaged': 'Mantente socialmente comprometido',
        'maintain_communication': 'Mantén hábitos de comunicación',
        'speech_patterns_healthy': '¡Los patrones de habla son saludables!',
        'keep_practicing_communication': 'Continúa practicando comunicación regular',
        'tongue_twisters_5': 'Práctica de trabalenguas (5 min diarios)',
        'exaggerate_mouth': 'Exagera los movimientos de la boca al hablar',
        'reading_slowly_clearly': 'Lee en voz alta lenta y claramente',
        'facial_muscle_exercises': 'Ejercicios de músculos faciales',
        'speak_slowly_deliberately': 'Habla lenta e deliberadamente',
        'take_pauses_sentences': 'Toma pausas entre oraciones',
        'speech_clarity_exercises': 'Los ejercicios de claridad de habla te ayudarán',
        'practice_makes_perfect': 'La práctica hace la perfección - ten paciencia contigo',
        'breathing_before_speaking': 'Ejercicios de respiración antes de hablar',
        'speak_slower_pace': 'Practica hablar a un ritmo más lento',
        'relaxation_techniques': 'Técnicas de relajación',
        'mindful_communication': 'Práctica de comunicación consciente',
        'take_breaks_conversations': 'Toma descansos durante conversaciones',
        'stress_affects_speech': 'El estrés afecta el habla - la relajación ayuda',
        'deep_breaths_speaking': 'Las respiraciones profundas antes de hablar pueden ayudar',
        'wonderful_emotional': '¡Wonderful estado emocional!',
        'positive_energy_valuable': 'Tu energía positiva es valiosa',
        'engage_enjoyable_activities': 'Participa en actividades agradables',
        'try_something_new': 'Intenta algo nuevo esta semana',
        'physical_exercise_mood': 'Ejercicio físico (impulsa el estado de ánimo)',
        'connect_friends_family': 'Conecta con amigos o familia',
        'practice_gratitude_daily': 'Practica gratitud diariamente',
        'spend_time_hobbies': 'Pasa tiempo en tus aficiones',
        'neutral_state_normal': 'Un estado neutral es normal',
        'small_activities_boost': 'Las pequeñas actividades pueden impulsar tu estado de ánimo',
        'deep_breathing_10': 'Ejercicios de respiración profunda (10 min, 2-3x/día)',
        'progressive_muscle': 'Relajación muscular progresiva',
        'nature_walks': 'Caminatas en la naturaleza',
        'prioritize_sleep_7_9': 'Prioriza el sueño (7-9 horas)',
        'limit_screen_time': 'Limita el tiempo de pantalla antes de dormir',
        'talk_someone_trust': 'Habla con alguien de confianza',
        'break_tasks_steps': 'Divide las tareas en pasos más pequeños',
        'stress_manageable': 'El estrés es manejable con las herramientas adecuadas',
        'be_kind_yourself': 'Sé amable contigo durante tiempos difíciles',
        'light_physical_walks': 'Actividad física ligera (caminatas, ejercicio suave)',
        'creative_expression': 'Expresión creativa (arte, música, escritura)',
        'reach_supportive': 'Alcanza a personas de apoyo',
        'maintain_routine': 'Mantén la rutina donde sea posible',
        'speak_counselor': 'Considera hablar con un consejero',
        'achievable_tasks': 'Participa en tareas pequeñas y alcanzables',
        'feelings_valid_temporary': 'Estos sentimientos son válidos y temporales',
        'support_available': 'El apoyo está disponible - no tienes que pasar por esto solo',
        'core_strengthening': 'Continúa ejercicios de fortalecimiento del núcleo',
        'maintain_flexibility': 'Mantén flexibilidad con estiramientos',
        'good_posture_habits': 'Continúa practicando buenos hábitos de postura',
        'movement_breaks': 'Toma descansos de movimiento regularmente',
        'excellent_posture': '¡Postura excelente!',
        'maintaining_prevents': 'Mantener una buena postura previene problemas futuros',
        'chin_tucks_10': 'Retracción de barbilla: Jala la barbilla hacia atrás (10 reps, 3x/día)',
        'neck_stretches': 'Estiramientos de cuello: Suave lado a lado y arriba abajo',
        'upper_back_strengthening': 'Fortalecimiento de espalda superior: Filas y pectorales invertidas',
        'chest_stretches_30': 'Estiramientos de pecho: Estiramiento de pared (30s, 3 reps)',
        'adjust_screen_height': 'Ajusta la altura de la pantalla al nivel de los ojos',
        'ergonomic_workspace': 'Usa configuración de espacio de trabajo ergonómico',
        'posture_check_reminders': 'Establece recordatorios de verificación de postura',
        'avoid_prolonged_phone': 'Evita el uso prolongado de teléfono',
        'forward_very_common': 'La postura de cabeza adelantada es muy común con el uso de pantalla',
        'small_adjustments_big': 'Los pequeños ajustes hacen grandes diferencias',
        'core_exercises_planks': 'Ejercicios de núcleo: Planchas, puentes (diarios)',
        'back_extensions_superman': 'Extensiones de espalda: Posición de Superman (10 reps, 2 sets)',
        'hip_flexor_stretches': 'Estiramientos de flexor de cadera (30s cada lado)',
        'shoulder_blade_squeezes': 'Aprieta de omóplatos (15 reps, 3x/día)',
        'use_lumbar_support': 'Usa apoyo lumbar al sentarte',
        'stand_up_30_minutes': 'Ponte de pie cada 30 minutos',
        'adjust_chair_height': 'Ajusta la altura de la silla correctamente',
        'sit_tall_shoulders': 'Practica estar sentado erguido con hombros hacia atrás',
        'slouching_stress_spine': 'Encorvarse pone tensión en tu columna vertebral',
        'building_core_strength': 'Construir fuerza del núcleo ayuda a mantener la postura',
        'great_job_maintaining': 'Excelente trabajo manteniendo',
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
        'light_aerobic_activities': 'হালকা এয়ারোবিক কার্যক্রম হৃদস্পন্দন ধীরে ধীরে বৃদ্ধি করতে',
        'gentle_walking_15_20': 'প্রতিদিন ১৫-২০ মিনিট মৃদু হাঁটাচলা',
        'stretching_flexibility': 'প্রসারণ এবং নমনীয়তা ব্যায়াম',
        'avoid_sudden_intense': 'হঠাৎ তীব্র কার্যক্রম এড়িয়ে চলুন',
        'stay_warm_comfortable': 'উষ্ণ এবং আরামদায়ক থাকুন',
        'monitor_feel_activities': 'কার্যক্রম চলাকালীন কীভাবে অনুভব করছেন তা পর্যবেক্ষণ করুন',
        'slow_heart_rate_detected': 'ধীর হৃদস্পন্দন সনাক্ত হয়েছে - আপনার স্বাস্থ্যসেবা প্রদানকারীর সাথে কথা বলুন',
        'gradual_increase_activity': 'ক্রমান্বয়ে কার্যক্রম বৃদ্ধি করা মূল চাবিকাঠি',
        'gentle_breathing_exercises': 'মৃদু শ্বাস-প্রশ্বাসের ব্যায়াম',
        'slow_paced_yoga_tai_chi': 'ধীর গতির যোগ বা তাই চি',
        'avoid_high_intensity': 'উচ্চ-তীব্রতার ওয়ার্কআউট অস্থায়ীভাবে এড়িয়ে চলুন',
        'reduce_caffeine_intake': 'ক্যাফেইন গ্রহণ কমিয়ে দিন',
        'practice_stress_management': 'চাপ ব্যবস্থাপনা অনুশীলন করুন',
        'ensure_adequate_rest': 'পর্যাপ্ত বিশ্রাম এবং ঘুম নিশ্চিত করুন',
        'elevated_heart_rate': 'উন্নত হৃদস্পন্দন সনাক্ত হয়েছে',
        'focus_relaxation_calm': 'শিথিলকরণ এবং শান্ত কার্যক্রমে মনোনিবেশ করুন',
        'low_impact_activities': 'কম প্রভাব কার্যক্রম তত্ত্বাবধানে',
        'seated_exercises_gentle': 'বসে থাকা ব্যায়াম এবং মৃদু নড়াচড়া',
        'avoid_strenuous': 'কঠোর পরিশ্রম এড়িয়ে চলুন',
        'monitor_heart_rate': 'নিয়মিত হৃদস্পন্দন পর্যবেক্ষণ করুন',
        'consult_healthcare': 'স্বাস্থ্যসেবা প্রদানকারীর সাথে পরামর্শ করুন',
        'keep_symptom_diary': 'একটি উপসর্গ ডায়েরি রাখুন',
        'irregular_rhythm_detected': 'অনিয়মিত ছন্দ সনাক্ত হয়েছে - চিকিৎসা পরামর্শ সুপারিশ করা হয়',
        'gentle_activity_safest': 'এই মুহূর্তে মৃদু কার্যক্রম সবচেয়ে নিরাপদ',
        'regular_physical_activity': 'নিয়মিত শারীরিক কার্যক্রম (৩০ মিনিট, সপ্তাহে ৫ দিন)',
        'mix_cardio_strength': 'কার্ডিও এবং শক্তি প্রশিক্ষণের মিশ্রণ',
        'maintain_balanced_meals': 'সুষম খাবার বজায় রাখুন',
        'continue_healthy_eating': 'স্বাস্থ্যকর খাওয়ার অভ্যাস অব্যাহত রাখুন',
        'glucose_well_controlled': 'গ্লুকোজ স্তর ভাল নিয়ন্ত্রিত!',
        'keep_monitoring_active': 'পর্যবেক্ষণ এবং সক্রিয় থাকা চালিয়ে যান',
        'light_activity_after': 'খাবারের পরে হালকা কার্যক্রম',
        'avoid_empty_stomach': 'খালি পেটে ব্যায়াম এড়িয়ে চলুন',
        'eat_small_frequent': 'ছোট, ঘন ঘন খাবার খান',
        'keep_healthy_snacks': 'স্বাস্থ্যকর খাবার সবসময় হাতের কাছে রাখুন',
        'monitor_blood_sugar': 'কার্যক্রমের আগে রক্ত শর্করা পর্যবেক্ষণ করুন',
        'low_glucose_detected': 'কম গ্লুকোজ সনাক্ত হয়েছে - নিয়মিত খাবার নিশ্চিত করুন',
        'carry_quick_carbs': 'দ্রুতকার্যকর কার্বোহাইড্রেট বহন করুন',
        'post_meal_walking': 'খাবারের পরে হাঁটাচলা (१५-२० मिनिट)',
        'strength_training_2_3': 'শক্তি প্রশিক্ষণ সপ্তাহে २-३ বার',
        'focus_whole_foods': 'পুরো খাবার এবং সবজিতে মনোনিবেশ করুন',
        'limit_refined_carbs': 'পরিমার্জিত কার্বোহাইড্রেট সীমিত করুন',
        'stay_well_hydrated': 'ভালোভাবে জলযুক্ত থাকুন',
        'elevated_glucose': 'উন্নত গ্লুকোজ সনাক্ত হয়েছে',
        'physical_activity_helps': 'শারীরিক কার্যক্রম রক্ত শর্করা নিয়ন্ত্রণে সাহায্য করে',
        'deep_breathing_5_min': 'গভীর শ্বাস-প্রশ্বাসের ব্যায়াম (প্রতিদিন ५ मिनिट)',
        'continue_current_activity': 'বর্তমান কার্যকলাপ স্তর অব্যাহত রাখুন',
        'good_air_quality': 'বাসস্থানে ভাল বায়ু গুণমান বজায় রাখুন',
        'stay_active_mobile': 'সক্রিয় এবং চলনশীল থাকুন',
        'breathing_pattern_healthy': 'শ্বাসের প্যাটার্ন সুস্থ!',
        'keep_practicing_breathing': 'ভাল শ্বাস-প্রশ্বাসের অভ্যাস অনুশীলন চালিয়ে যান',
        'core_strengthening': 'মূল শক্তিশালী করার ব্যায়াম অব্যাহত রাখুন',
        'maintain_flexibility': 'প্রসারণের সাথে নমনীয়তা বজায় রাখুন',
        'good_posture_habits': 'ভাল মুদ্রার অভ্যাস অনুশীলন করতে থাকুন',
        'movement_breaks': 'নিয়মিত চলাফেরার বিরতি নিন',
        'excellent_posture': 'চমৎকার মুদ্রা!',
        'maintaining_prevents': 'ভাল মুদ্রা বজায় রাখা ভবিষ্যতের সমস্যা প্রতিরোধ করে',
    },
    # Marathi - मराठी
    'mr': {
        'heart_health': 'हृदय आरोग्य',
        'blood_glucose': 'रक्त ग्लूकोज',
        'breathing_health': 'श्वसन आरोग्य',
        'speech_communication': 'भाषण आणि संचार',
        'emotional_wellbeing': 'भावनिक कल्याण',
        'posture_health': 'भाव आरोग्य',
        'exercises_activities': 'व्यायाम आणि क्रियाकलाप',
        'lifestyle_tips': 'जीवनशैली सुझाव',
        'important_notes': 'महत्वाचे नोट्स',
        'continue_moderate_aerobic': 'मध्यम एरोबिक व्यायाम सुरू ठेवा (२०-३० मिनिटे, आठवड्यातून ३-४ वेळा)',
        'walking_swimming_cycling': 'आरामदायक गतीने चालणे, तरंगणे किंवा सायकल चालवणे',
        'maintain_current_healthy': 'आपल्या सद्य आरोग्यकर अभ्यासांची देखभाल करा',
        'stay_hydrated': 'दिनभर हायड्रेटेड राहा',
        'heart_rhythm_healthy': 'आपली हृदय गती आरोग्यकर आहे!',
        'keep_up_good_work': 'नियमित क्रियाकलापांसह चांगले काम सुरू ठेवा',
        'light_aerobic_activities': 'हृदय गती हळूहळू वाढवण्यासाठी हलके एरोबिक क्रियाकलाप',
        'gentle_walking_15_20': 'दैनिक १५-२० मिनिटांची सौम्य पदयात्रा',
        'stretching_flexibility': 'स्ट्रेचिंग आणि लवचिकता व्यायाम',
        'avoid_sudden_intense': 'अचानक तीव्र क्रियाकलाप टाळा',
        'stay_warm_comfortable': 'उष्ण आणि आरामदायक राहा',
        'monitor_feel_activities': 'क्रियाकलाप करताना आप्ण कसे वाटत आहे ते लक्ष्य द्या',
        'slow_heart_rate_detected': 'मंद हृदय गती शोधली गेली - आपल्या आरोग्यसेवा प्रदानकर्त्याशी बोला',
        'gradual_increase_activity': 'क्रियाकलापात क्रमिक वाढ मुख्य आहे',
        'gentle_breathing_exercises': 'सौम्य श्वास व्यायाम',
        'slow_paced_yoga_tai_chi': 'मंद गतीच्या योग किंवा ताई ची',
        'avoid_high_intensity': 'उच्च-तीव्रता कसरत तात्पुरते टाळा',
        'reduce_caffeine_intake': 'कॅफेइन सेवन कमी करा',
        'practice_stress_management': 'तणाव व्यवस्थापन सराव करा',
        'ensure_adequate_rest': 'पर्याप्त विश्राम आणि झोप सुनिश्चित करा',
        'elevated_heart_rate': 'उन्नत हृदय गती शोधली गेली',
        'focus_relaxation_calm': 'विश्राम आणि शांत क्रियाकलापांवर लक्ष केंद्रित करा',
        'low_impact_activities': 'पर्यवेक्षणाखाली कमी प्रभाव क्रियाकलाप',
        'seated_exercises_gentle': 'बसलेल्या व्यायाम आणि सौम्य हालचाल',
        'avoid_strenuous': 'कठोर क्रियाकलाप टाळा',
        'monitor_heart_rate': 'नियमितपणे हृदय गती मॉनिटर करा',
        'consult_healthcare': 'आरोग्यसेवा प्रदानकर्त्यांशी सल्ला करा',
        'keep_symptom_diary': 'लक्षण डायरी ठेवा',
        'irregular_rhythm_detected': 'अनियमित लय शोधली गेली - वैद्यकीय सल्ल्याची शिफारस केली जाते',
        'gentle_activity_safest': 'सध्या सौम्य क्रियाकलाप सर्वात सुरक्षित आहे',
        'regular_physical_activity': 'नियमित शारीरिक क्रियाकलाप (३० मिनिटे, आठवड्यातून ५ दिवस)',
        'mix_cardio_strength': 'कार्डिओ आणि शक्ती प्रशिक्षणाचे मिश्रण',
        'maintain_balanced_meals': 'संतुलित जेवण ठेवा',
        'continue_healthy_eating': 'निरोगी खाण्याची आदत सुरू ठेवा',
        'glucose_well_controlled': 'ग्लूकोज पातळी चांगल्या नियंत्रणात आहे!',
        'keep_monitoring_active': 'मॉनिटरिंग सुरू ठेवा आणि सक्रिय राहा',
        'light_activity_after': 'जेवणानंतर हल्का क्रियाकलाप',
        'avoid_empty_stomach': 'रिक्त पोटे व्यायाम करणे टाळा',
        'eat_small_frequent': 'लहान, वारंवार जेवणे खा',
        'keep_healthy_snacks': 'निरोगी स्नॅक्स उपलब्ध ठेवा',
        'monitor_blood_sugar': 'क्रियाकलापपूर्वी रक्तातील साखर मॉनिटर करा',
        'low_glucose_detected': 'कमी ग्लूकोज शोधला गेला - नियमित जेवण सुनिश्चित करा',
        'carry_quick_carbs': 'द्रुत कार्यरत कार्बोहायड्रेट वहन करा',
        'post_meal_walking': 'जेवणानंतर चालणे (१५-२० मिनिटे)',
        'strength_training_2_3': 'सप्ताहातून २-३ वेळा शक्ती प्रशिक्षण',
        'focus_whole_foods': 'संपूर्ण अन्न आणि भाज्यांवर लक्ष केंद्रित करा',
        'limit_refined_carbs': 'परिष्कृत कार्बोहायड्रेट मर्यादित करा',
        'stay_well_hydrated': 'चांगल्या जलयुक्ত राहा',
        'elevated_glucose': 'उन्नत ग्लूकोज शोधला गेला',
        'physical_activity_helps': 'शारीरिक क्रियाकलाप रक्तातील साखर नियंत्रित करण्यास मदत करते',
        'deep_breathing_5_min': 'गहन श्वास व्यायाम (दैनिक ५ मिनिटे)',
        'continue_current_activity': 'सद्य क्रियाकलाप पातळी सुरू ठेवा',
        'good_air_quality': 'राहत्याच्या ठिकाणी चांगली हवा गुणवत्ता बनवून ठेवा',
        'stay_active_mobile': 'सक्रिय आणि गतिशील राहा',
        'breathing_pattern_healthy': 'श्वास पद्धती आरोग्यकर आहे!',
        'keep_practicing_breathing': 'चांगल्या श्वास सराव करणे सुरू ठेवा',
        'diaphragmatic_breathing': 'डायाफ्राग्मिक श्वास: पोटात खोलवर श्वास घ्या (५-१० मिनिटे, दिवसातून ३ वेळा)',
        'box_breathing': 'बॉक्स श्वास: ४ से.ला श्वास घ्या, ४ से.साठी धरा, ४ से.साठी श्वास सोडा, ४ से.साठी धरा',
        'gentle_chest_expansion': 'सौम्य छाती विस्तार व्यायाम',
        'good_posture_sitting': 'बसल्या वेळी चांगली मुद्रा सराव करा',
        'breathing_breaks_hour': 'दर तासाला श्वास विश्राम घ्या',
        'avoid_restrictive': 'प्रतिबंधक कपडे टाळा',
        'shallow_breathing_detected': 'उथळ श्वास शोधला गेला - गहन श्वासांवर लक्ष केंद्रित करा',
        'lungs_hold_more_air': 'आपले फुफ्फुस सरावाने अधिक हवा धरू शकतात',
        'paced_breathing': 'गतीचा श्वास: श्वास घेताना ४ मिनिटे गिनती, ६ मिनिटे श्वास सोडा',
        'relaxed_breathing_exercises': 'शांत श्वास व्यायाम',
        'gentle_yoga_breath': 'श्वासावर केंद्रित असलेला सौम्य योग',
        'reduce_stress_possible': 'शक्य तितके तणाव कमी करा',
        'practice_mindfulness': 'मनःस्थिति सराव करा',
        'monitor_breathing_patterns': 'श्वास पद्धती मॉनिटर करा',
        'irregular_breathing_noticed': 'अनियमित श्वास पद्धती लक्षात आली',
        'regular_practice_improves': 'नियमित सराव श्वास लय सुधारते',
        'breathing_awareness': 'श्वास जागरूकता व्यायाम',
        'gentle_aerobic_activity': 'सौम्य एरोबिक क्रियाकलाप',
        'consult_sleep_specialist': 'झोप विशेषज्ञांशी सल्ला करा',
        'sleep_on_side': 'आपल्या बाजूला झोपा',
        'maintain_healthy_weight': 'निरोगी वजन ठेवा',
        'avoid_alcohol_bed': 'झोपण्यापूर्वी अल्कोहोल टाळा',
        'potential_apnea_risk': 'संभाव्य अ॥्निया जोखीम - वैद्यकीय मूल्यांकन शिफारस केली जाते',
        'good_sleep_position': 'चांगली झोपेची स्थिती श्वासास मदत करते',
        'continue_conversation': 'नियमित संभाषण सराव सुरू ठेवा',
        'reading_aloud_10': 'दैनिक १० मिनिटांसाठी मोठ्याने वाचन',
        'stay_socially_engaged': 'सामाजिकदृष्ट्या व्यस्त राहा',
        'maintain_communication': 'संवाद आदती ठेवा',
        'speech_patterns_healthy': 'भाषण पद्धती आरोग्यकर आहे!',
        'keep_practicing_communication': 'नियमित संवाद सराव सुरू ठेवा',
        'tongue_twisters_5': 'जिभा मोडे सराव (दैनिक ५ मिनिटे)',
        'exaggerate_mouth': 'बोलताना तोंड हालचालीचे बढती करा',
        'reading_slowly_clearly': 'हळूच आणि स्पष्टपणे मोठ्याने वाचन',
        'facial_muscle_exercises': 'चेहरे स्नायु व्यायाम',
        'speak_slowly_deliberately': 'हळूच आणि इच्छेने बोला',
        'take_pauses_sentences': 'वाक्यामध्ये विराम घ्या',
        'speech_clarity_exercises': 'भाषण स्पष्टता व्यायाम मदत करेल',
        'practice_makes_perfect': 'सराव परिपूर्ण करते - स्वतःशी धैर्य धरा',
        'breathing_before_speaking': 'बोलण्यापूर्वी श्वास व्यायाम',
        'speak_slower_pace': 'धीमे गतीने बोलण्याचा सराव करा',
        'relaxation_techniques': 'विश्राम तंत्र',
        'mindful_communication': 'सचेत संवाद सराव',
        'take_breaks_conversations': 'संभाषण दरम्यान विश्राम घ्या',
        'stress_affects_speech': 'तणाव भाषण प्रभावित करते - विश्राम मदत करते',
        'deep_breaths_speaking': 'बोलण्यापूर्वी गहन श्वास मदत करू शकते',
        'wonderful_emotional': 'अद्भुत भावनिक अवस्था!',
        'positive_energy_valuable': 'आपली सकारात्मक ऊर्जा मूल्यवान आहे',
        'engage_enjoyable_activities': 'आनंदमय क्रियाकलापांमध्ये गुंता',
        'try_something_new': 'या आठवड्यात काहीतरी नवीन करून पहा',
        'physical_exercise_mood': 'शारीरिक व्यायाम (मनोदशा वाढवते)',
        'connect_friends_family': 'मित्रांशी किंवा कुटुंबाशी जोडिला',
        'practice_gratitude_daily': 'दररोज कृतज्ञता सराव करा',
        'spend_time_hobbies': 'छंदावर वेळ घालवा',
        'neutral_state_normal': 'तटस्थ स्थिती सामान्य आहे',
        'small_activities_boost': 'लहान क्रियाकलाप आपली मनोदशा सुधारू शकतात',
        'deep_breathing_10': 'गहन श्वास व्यायाम (१० मिनिटे, दिवसातून २-३ वेळा)',
        'progressive_muscle': 'प्रगतीशील स्नायु विश्राम',
        'nature_walks': 'निसर्गातील फेरे',
        'prioritize_sleep_7_9': 'झोपकी प्राधान्य द्या (७-९ तास)',
        'limit_screen_time': 'झोपण्यापूर्वी स्क्रीन वेळ मर्यादित करा',
        'talk_someone_trust': 'विश्वसनीय व्यक्तीशी बोला',
        'break_tasks_steps': 'कार्य लहान पायऱ्यांमध्ये विभाजित करा',
        'stress_manageable': 'योग्य साधनांसह तणाव प्रबंधनीय आहे',
        'be_kind_yourself': 'कठीण काळात स्वतःशी दयाळू व्हा',
        'light_physical_walks': 'हल्का शारीरिक क्रियाकलाप (चालणे, सौम्य व्यायाम)',
        'creative_expression': 'रचनात्मक अभिव्यक्ती (कला, संगीत, लेखन)',
        'reach_supportive': 'सहायक लोकांकडे पोहोचा',
        'maintain_routine': 'संभव तितके दिनचर्या ठेवा',
        'speak_counselor': 'सल्लागारांशी बोलण्याचा विचार करा',
        'achievable_tasks': 'लहान, साध्य कार्यांमध्ये गुंता',
        'feelings_valid_temporary': 'या भावना वैध आणि तात्पुरत्या आहेत',
        'support_available': 'समर्थन उपलब्ध आहे - आपल्याला याच्या मधून एकटे गेण्याची आवश्यकता नाही',
        'core_strengthening': 'मूळ मजबूतीकरण व्यायाम सुरू ठेवा',
        'maintain_flexibility': 'स्ट्रेचिंगद्वारे लवचिकता ठेवा',
        'good_posture_habits': 'चांगल्या मुद्रा आदती सराव सुरू ठेवा',
        'movement_breaks': 'नियमितपणे हालचाल विश्राम घ्या',
        'excellent_posture': 'उत्कृष्ट मुद्रा!',
        'maintaining_prevents': 'चांगली मुद्रा ठेवल्याने भविष्यातील समस्या टाळता येतात',
        'chin_tucks_10': 'हनुवटी खेचणे: हनुवटी मागे खेचा (१० पुनरावृत्ती, दिवसातून ३ वेळा)',
        'neck_stretches': 'मानेच्या स्ट्रेचे: सौम्य बाजू-दर-बाजू आणि वर-खाली',
        'upper_back_strengthening': 'वरच्या पोलादच्या मजबूतीकरण: पंक्ती आणि उलट माहिनी',
        'chest_stretches_30': 'छाती स्ट्रेचे: दरवाजा स्ट्रेच (३० से., ३ पुनरावृत्ती)',
        'adjust_screen_height': 'स्क्रीनची उंची डोळ्यांच्या स्तरावर समायोजित करा',
        'ergonomic_workspace': 'एर्गोनॉमिक कार्यस्थल सेटअप वापरा',
        'posture_check_reminders': 'मुद्रा तपासणी स्मारके सेट करा',
        'avoid_prolonged_phone': 'फोनचा दीर्घ वापर टाळा',
        'forward_very_common': 'स्क्रीन वापराने पुढे सिर मुद्रा अत्यंत सामान्य आहे',
        'small_adjustments_big': 'लहान समायोजन मोठे फरक करते',
        'core_exercises_planks': 'मूळ व्यायाम: तख्ती, पुल (दैनिक)',
        'back_extensions_superman': 'पीठ विस्तार: सुपरमॅन पोज (१० पुनरावृत्ती, २ सेट)',
        'hip_flexor_stretches': 'हिप फ्लेक्सर स्ट्रेचे (३० से. प्रत्येक बाजू)',
        'shoulder_blade_squeezes': 'खांद्याच्या पत्र्याची अंकिती (१५ पुनरावृत्ती, दिवसातून ३ वेळा)',
        'use_lumbar_support': 'बसल्या वेळी काठीच्या समर्थन वापरा',
        'stand_up_30_minutes': 'दर ३० मिनिटांना उभे राहा',
        'adjust_chair_height': 'खुर्चीची उंची योग्यरित्या समायोजित करा',
        'sit_tall_shoulders': 'खांद्यांसह सरळ बसण्याचा सराव करा',
        'slouching_stress_spine': 'झुकणे आपल्या मेरुदंडावर दबाव टाकते',
        'building_core_strength': 'मूळ शक्तीची निर्मिती मुद्रा ठेवण्यास मदत करते',
        'great_job_maintaining': 'आप्ण जे ठेवत आहात त्यात चांगले काम',
        'focus_areas_improvement': 'सुधारणेचे क्षेत्र',
        'follow_recommendations': 'आपली पुनर्वसन यात्रा समर्थित करण्यासाठी खालील शिफारसी अनुसरण करा।',
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

# Add fallback entries for all languages - use English as default
for lang_code in ['en', 'es', 'hi', 'bn', 'mr', 'ta', 'kn', 'te', 'or', 'pa', 'hry', 'gu', 'bho', 'ur']:
    if lang_code not in RECOMMENDATIONS_TRANSLATIONS:
        # Create a copy of English dictionary as fallback for missing languages
        RECOMMENDATIONS_TRANSLATIONS[lang_code] = RECOMMENDATIONS_TRANSLATIONS['en'].copy()

# Quality fallback: where selected regional dictionaries still equal English,
# prefer Hindi text while preserving explicit native entries.
for lang_code in ['mr', 'ta', 'kn', 'te', 'or', 'pa', 'hry', 'gu', 'bho', 'ur']:
    for key, en_value in RECOMMENDATIONS_TRANSLATIONS['en'].items():
        if RECOMMENDATIONS_TRANSLATIONS.get(lang_code, {}).get(key) == en_value and key in RECOMMENDATIONS_TRANSLATIONS['hi']:
            RECOMMENDATIONS_TRANSLATIONS[lang_code][key] = RECOMMENDATIONS_TRANSLATIONS['hi'][key]

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
    
    if status == 'status_normal':
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
    
    elif status == 'status_bradycardia':
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
    
    elif status == 'status_tachycardia':
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
    
    elif status == 'status_irregular':
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
    
    if range_label == 'status_normal':
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
    
    elif range_label == 'status_low':
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
    
    elif range_label == 'status_high':
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
    
    if status == 'status_normal':
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
    
    elif status == 'status_shallow_breathing':
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
    
    elif status == 'status_irregular':
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
    
    elif status == 'status_apnea_risk':
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
    
    if pattern == 'status_normal_speech':
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
    
    elif pattern == 'status_slurred_speech':
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
    
    elif pattern == 'status_stressed_speech':
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
    
    if state == 'status_happy':
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
    
    elif state == 'status_neutral':
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
    
    elif state == 'status_stressed':
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
    
    elif state == 'status_sad':
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
    
    if posture_type == 'status_good_posture':
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
    
    elif posture_type == 'status_forward_head':
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
    
    elif posture_type == 'status_slouched':
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
    
    # Check each prediction using status keys and translated labels
    if 'heartbeat' in predictions:
        if predictions['heartbeat']['status'] != 'status_normal':
            issues.append(t('heart_health'))
        else:
            strengths.append(t('heart_health'))
    
    if 'glucose' in predictions:
        if predictions['glucose']['range'] != 'status_normal':
            issues.append(t('blood_glucose'))
        else:
            strengths.append(t('blood_glucose'))
    
    if 'breathing' in predictions:
        if predictions['breathing']['status'] != 'status_normal':
            issues.append(t('breathing_health'))
        else:
            strengths.append(t('breathing_health'))
    
    if 'speech' in predictions:
        if predictions['speech']['pattern'] != 'status_normal_speech':
            issues.append(t('speech_communication'))
        else:
            strengths.append(t('speech_communication'))
    
    if 'emotion' in predictions:
        if predictions['emotion']['state'] in ['status_stressed', 'status_sad']:
            issues.append(t('emotional_wellbeing'))
        else:
            strengths.append(t('emotional_wellbeing'))
    
    if 'posture' in predictions:
        if predictions['posture']['posture'] != 'status_good_posture':
            issues.append(t('posture_health'))
        else:
            strengths.append(t('posture_health'))
    
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