import os
import sqlite3
from datetime import datetime

def add_user(username, email):
    DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'mental_health.db')
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    
    cursor.execute('SELECT user_id FROM Users WHERE email = ?', (email,))
    existing_user = cursor.fetchone()

    if existing_user:
        print(f"User with email {email} already exists!")
        conn.close()
        return existing_user[0]

    
    cursor.execute('''
        INSERT INTO Users (username, email, created_at)
        VALUES (?, ?, ?)
    ''', (username, email, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    print(f"User {username} added successfully with user_id {user_id}!")
    return user_id