import os
import sqlite3

def get_baseline(user_id, parameter_name):
    DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'mental_health.db')
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT baseline_value FROM Baselines
        WHERE user_id = ? AND parameter_name = ?
    ''', (user_id, parameter_name))

    result = cursor.fetchone()
    conn.close()

    if result:
        return result[0]
    else:
        print(f"No baseline found for user {user_id} and parameter {parameter_name}")
        return None

def get_all_baselines(user_id):
    DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'mental_health.db')
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT parameter_name, baseline_value FROM Baselines
        WHERE user_id = ?
    ''', (user_id,))

    results = cursor.fetchall()
    conn.close()

    if results:
        baselines = {row[0]: row[1] for row in results}
        return baselines
    else:
        print(f"No baselines found for user {user_id}")
        return None