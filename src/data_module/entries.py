import os
import sqlite3
from data_module.baseline import calculate_baseline

def add_entry(user_id, journal_text, sentiment_score, stress, anxiety, sadness, 
              frustration, emotional_exhaustion, optimism, motivation, task_engagement,
              social_connectedness, social_support, self_efficacy, coping_ability,
              resilience, concentration, mental_fatigue, rumination, self_talk_score,
              sleep_quality, sleep_duration, physical_fatigue, cognitive_functioning):
    
    DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'mental_health.db')
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO Entries (
            user_id, journal_text, sentiment_score, stress, anxiety, sadness,
            frustration, emotional_exhaustion, optimism, motivation, task_engagement,
            social_connectedness, social_support, self_efficacy, coping_ability,
            resilience, concentration, mental_fatigue, rumination, self_talk_score,
            sleep_quality, sleep_duration, physical_fatigue, cognitive_functioning
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, journal_text, sentiment_score, stress, anxiety, sadness,
          frustration, emotional_exhaustion, optimism, motivation, task_engagement,
          social_connectedness, social_support, self_efficacy, coping_ability,
          resilience, concentration, mental_fatigue, rumination, self_talk_score,
          sleep_quality, sleep_duration, physical_fatigue, cognitive_functioning))

    conn.commit()
    conn.close()
    print("Entry added successfully!")
    calculate_baseline(user_id)   
    