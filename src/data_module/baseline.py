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

# Flat, single-entry multipliers. No decay — applies only to the entry
# immediately following the flagged one (day-by-day, not a multi-day fade).
PROTECT_MULTIPLIER = 0.1
ADAPT_MULTIPLIER = 3.0


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
        # Replaces any missing database values (None) with 0.0 to prevent math crashes
        values = np.array([float(entry[i + 1]) if entry[i + 1] is not None else 0.0 for entry in entries])

        if param in LONG_TERM_PARAMETERS:
            baseline_value = values[-1]
            std_dev_value = float(np.std(values)) if len(values) > 1 else 0.0
        else:
            mean = np.mean(values)
            std = np.std(values)
            final_weights = recency_weights.copy()

            if len(entries) > 20:
                for j, value in enumerate(values):
                    if abs(value - mean) > 2 * std:
                        final_weights[j] *= 0.1

            # Day-by-day anomaly weighting: each entry's weight is adjusted
            # based on the PREVIOUS entry's flag for this parameter (not its
            # own flag). No decay across multiple entries — the effect
            # applies to exactly one entry, then resets to normal.
            for j in range(1, len(entries)):
                previous_status = parsed_flags[j - 1].get(param, 'normal').lower()
                if previous_status == 'protect':
                    final_weights[j] *= PROTECT_MULTIPLIER
                elif previous_status == 'adapt':
                    final_weights[j] *= ADAPT_MULTIPLIER
                # 'normal' (or no flag / before anomaly detection kicks in
                # at entry 27) leaves the weight unchanged.

            baseline_value = np.average(values, weights=final_weights)
            variance = np.average((values - baseline_value) ** 2, weights=final_weights)
            std_dev_value = float(np.sqrt(variance))

        cursor.execute('''
            INSERT OR REPLACE INTO Baselines (user_id, parameter_name, baseline_value, std_dev, last_updated)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, param, baseline_value, std_dev_value, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

    conn.commit()
    conn.close()
    print(f"Baseline calculated and saved for user {user_id}!")
