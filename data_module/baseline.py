import sqlite3
import numpy as np
from datetime import datetime

PARAMETERS = [
    'sentiment_score', 'stress', 'anxiety', 'sadness', 'frustration',
    'emotional_exhaustion', 'optimism', 'motivation', 'task_engagement',
    'social_connectedness', 'social_support', 'self_efficacy', 'coping_ability',
    'resilience', 'concentration', 'mental_fatigue', 'rumination', 'self_talk_score',
    'sleep_quality', 'sleep_duration', 'physical_fatigue', 'cognitive_functioning'
]

DECAY_FACTOR = 0.1

def calculate_baseline(user_id):
    conn = sqlite3.connect('mental_health.db')
    cursor = conn.cursor()

    
    cursor.execute('''
        SELECT timestamp, sentiment_score, stress, anxiety, sadness, frustration,
               emotional_exhaustion, optimism, motivation, task_engagement,
               social_connectedness, social_support, self_efficacy, coping_ability,
               resilience, concentration, mental_fatigue, rumination, self_talk_score,
               sleep_quality, sleep_duration, physical_fatigue, cognitive_functioning
        FROM Entries
        WHERE user_id = ?
        ORDER BY timestamp DESC
    ''', (user_id,))

    entries = cursor.fetchall()

    if not entries:
        print("No entries found for this user.")
        conn.close()
        return

    
    now = datetime.now()
    weights = []

    for entry in entries:
        timestamp = datetime.strptime(entry[0], '%Y-%m-%d %H:%M:%S')
        days_ago = (now - timestamp).total_seconds() / 86400
        weight = np.exp(-DECAY_FACTOR * days_ago)
        weights.append(weight)

    weights = np.array(weights)

   
    for i, param in enumerate(PARAMETERS):
        values = np.array([entry[i + 1] for entry in entries])

        # Outlier dampening
        mean = np.mean(values)
        std = np.std(values)
        dampened_weights = weights.copy()

        for j, value in enumerate(values):
            if abs(value - mean) > 2 * std:
                dampened_weights[j] *= 0.1


        baseline_value = np.average(values, weights=dampened_weights)

        
        cursor.execute('''
            INSERT OR REPLACE INTO Baselines (user_id, parameter_name, baseline_value, last_updated)
            VALUES (?, ?, ?, ?)
        ''', (user_id, param, baseline_value, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

    conn.commit()
    conn.close()
    print(f"Baseline calculated and saved for user {user_id}!")

