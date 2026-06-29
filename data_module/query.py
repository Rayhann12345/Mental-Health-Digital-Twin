import sqlite3

def get_baseline(user_id, parameter_name):
    conn = sqlite3.connect('mental_health.db')
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
    conn = sqlite3.connect('mental_health.db')
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