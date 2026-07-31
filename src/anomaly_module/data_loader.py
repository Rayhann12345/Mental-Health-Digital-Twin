import os
import sqlite3
import json

def get_db_connection():

    base_dir = os.path.dirname(os.path.dirname(__file__))
    db_path = os.path.join(base_dir, 'mental_health.db')
    
    # Enable row factory to easily access columns by their name
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def get_user_entry_count(user_id, parameter_name=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if parameter_name:
        query = f'SELECT COUNT({parameter_name}) FROM Entries WHERE user_id = ?'
    else:
        query = 'SELECT COUNT(*) FROM Entries WHERE user_id = ?'
        
    cursor.execute(query, (user_id,))
    count = cursor.fetchone()[0]
    
    conn.close()
    return count

def load_anomaly_inputs(user_id):

    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM Entries 
        WHERE user_id = ? 
        ORDER BY timestamp DESC LIMIT 1
    ''', (user_id,))
    latest_entry = cursor.fetchone()

    if not latest_entry:
        conn.close()
        raise ValueError(f"No journal entries found for user_id: {user_id}")


    cursor.execute('''
        SELECT parameter_name, baseline_value, std_dev 
        FROM Baselines 
        WHERE user_id = ?
    ''', (user_id,))
    baselines_data = cursor.fetchall()
    conn.close()

    # Convert baselines into a quick lookup dictionary
    
    baseline_lookup = {
        row['parameter_name']: {
            'baseline': row['baseline_value'], 
            'std_dev': row['std_dev']
        } 
        for row in baselines_data
    }


    long_window_params = {
        "self_efficacy", 
        "coping_ability", 
        "social_connectedness", 
        "social_support"
    }


    excluded_columns = {'entry_id', 'user_id', 'timestamp', 'journal_text'}

    evaluation_inputs = []
    
    for key in latest_entry.keys():
        if key not in excluded_columns and key in baseline_lookup:
            param_name = key
            current_value = latest_entry[key]
            baseline = baseline_lookup[key]['baseline']
            std_dev = baseline_lookup[key]['std_dev']
            
            max_window_length = 14 if param_name in long_window_params else 7

            cursor.execute('''
                SELECT window_data FROM SlidingWindows 
                WHERE user_id = ? AND parameter_name = ?
            ''', (user_id, param_name))
            result = cursor.fetchone()
            
            if result:
                historical_window = json.loads(result['window_data']) 
            else:
                historical_window = []
            
            evaluation_inputs.append({
                "param_name": param_name,
                "current_value": current_value,
                "baseline": baseline,
                "std_dev": std_dev,
                "historical_window": historical_window,
                "max_window_length": max_window_length
            })

    return evaluation_inputs

def update_sliding_window(user_id, param_name, updated_window):

    conn = get_db_connection()
    cursor = conn.cursor()
    
    window_string = json.dumps(updated_window)
    
    cursor.execute('''
        REPLACE INTO SlidingWindows (user_id, parameter_name, window_data, last_updated)
        VALUES (?, ?, ?, CURRENT_TIMESTAMP)
    ''', (user_id, param_name, window_string))
    
    conn.commit()
    conn.close()
