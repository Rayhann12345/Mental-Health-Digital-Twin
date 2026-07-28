import os
import sqlite3
import json
import numpy as np
from datetime import datetime

PARAMETERS = [
    'sentiment_score', 'stress', 'anxiety', 'sadness', 'frustration',
    'emotional_exhaustion', 'optimism', 'motivation', 'task_engagement',
    'social_connectedness', 'social_support', 'self_efficacy', 'coping_ability',
    'resilience', 'concentration', 'mental_fatigue', 'rumination', 'self_talk_score',
    'sleep_quality', 'physical_fatigue'
]

# Parameters where the baseline is just the most recent value, not an average
LONG_TERM_PARAMETERS = [
    'rumination', 'resilience', 'mental_fatigue', 'physical_fatigue', 'emotional_exhaustion'
]

DECAY_FACTOR = 0.1

# Decaying multipliers applied starting at the flagged entry, fading back to normal
PROTECT_MULTIPLIERS = [0.1, 0.3, 0.6]
ADAPT_MULTIPLIERS = [3.0, 2.0, 1.5]


def calculate_baseline(user_id):
    DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'mental_health.db')
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT timestamp, sentiment_score, stress, anxiety, sadness, frustration,
               emotional_exhaustion, optimism, motivation, task_engagement,
               social_connectedness, social_support, self_efficacy, coping_ability,
               resilience, concentration, mental_fatigue, rumination, self_talk_score,
               sleep_quality, physical_fatigue, anomaly_flags
        FROM Entries
        WHERE user_id = ?
        ORDER BY timestamp ASC
    ''', (user_id,))

    entries = cursor.fetchall()

    if not entries:
        print("No entries found for this user.")
        conn.close()
        return

    now = datetime.now()

    recency_weights = []
    for entry in entries:
        timestamp = datetime.strptime(entry[0], '%Y-%m-%d %H:%M:%S')
        days_ago = (now - timestamp).total_seconds() / 86400
        recency_weights.append(np.exp(-DECAY_FACTOR * days_ago))
    recency_weights = np.array(recency_weights)

    # Parse anomaly flags per entry (last column)
    parsed_flags = [json.loads(entry[-1]) if entry[-1] else {} for entry in entries]

    for i, param in enumerate(PARAMETERS):
        values = np.array([entry[i + 1] for entry in entries])

        if param in LONG_TERM_PARAMETERS:
            baseline_value = values[-1]
        else:
            mean = np.mean(values)
            std = np.std(values)
            final_weights = recency_weights.copy()

            if len(entries) > 15:
                for j, value in enumerate(values):
                    if abs(value - mean) > 2 * std:
                        final_weights[j] *= 0.1

            active_status = None
            steps_remaining = 0

            for j, flags in enumerate(parsed_flags):
                status = flags.get(param, 'normal').lower()  # <-- case-insensitive fix

                if status in ('protect', 'adapt'):
                    active_status = status
                    steps_remaining = 3

                if active_status and steps_remaining > 0:
                    step_index = 3 - steps_remaining
                    if active_status == 'protect':
                        final_weights[j] *= PROTECT_MULTIPLIERS[step_index]
                    elif active_status == 'adapt':
                        final_weights[j] *= ADAPT_MULTIPLIERS[step_index]
                    steps_remaining -= 1
                    if steps_remaining == 0:
                        active_status = None

            baseline_value = np.average(values, weights=final_weights)

        cursor.execute('''
            INSERT OR REPLACE INTO Baselines (user_id, parameter_name, baseline_value, last_updated)
            VALUES (?, ?, ?, ?)
        ''', (user_id, param, baseline_value, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

    conn.commit()
    conn.close()
    print(f"Baseline calculated and saved for user {user_id}!")