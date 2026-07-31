import sqlite3
import os

def get_db_connection():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    db_path = os.path.join(base_dir, 'mental_health.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def get_user_id_by_email(email):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT user_id FROM Users WHERE email = ?', (email,))
    result = cursor.fetchone()
    
    if result:
        user_id = result['user_id']
    else:
        username = email.split('@')[0]
        cursor.execute('INSERT INTO Users (username, email) VALUES (?, ?)', (username, email))
        user_id = cursor.lastrowid
        
    conn.commit()
    conn.close()
    return user_id

def get_recent_journals(user_id, limit=13):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT journal_text FROM Entries 
        WHERE user_id = ? AND journal_text IS NOT NULL
        ORDER BY timestamp DESC LIMIT ?
    ''', (user_id, limit))
    
    rows = cursor.fetchall()
    entries = [row['journal_text'] for row in reversed(rows)]
    conn.close()
    return entries

def save_new_entry(user_id, journal_text, scores):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    columns = ['user_id', 'journal_text'] + list(scores.keys())
    placeholders = ', '.join(['?'] * len(columns))
    values = [user_id, journal_text] + list(scores.values())
    
    query = f'''
        INSERT INTO Entries ({', '.join(columns)}) 
        VALUES ({placeholders})
    '''
    cursor.execute(query, values)
    conn.commit()
    conn.close()
