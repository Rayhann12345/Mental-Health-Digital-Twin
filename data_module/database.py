import os
import sqlite3

def create_database():

    DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'mental_health.db')
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Entries (
            entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            journal_text TEXT,
            sentiment_score REAL,
            stress REAL,
            anxiety REAL,
            sadness REAL,
            frustration REAL,
            emotional_exhaustion REAL,
            optimism REAL,
            motivation REAL,
            task_engagement REAL,
            social_connectedness REAL,
            social_support REAL,
            self_efficacy REAL,
            coping_ability REAL,
            resilience REAL,
            concentration REAL,
            mental_fatigue REAL,
            rumination REAL,
            self_talk_score REAL,
            sleep_quality REAL,
            sleep_duration REAL,
            physical_fatigue REAL,
            cognitive_functioning REAL,
            FOREIGN KEY (user_id) REFERENCES Users(user_id)
        )
    ''')

   
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Baselines (
            user_id INTEGER,
            parameter_name TEXT,
            baseline_value REAL,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (user_id, parameter_name),
            FOREIGN KEY (user_id) REFERENCES Users(user_id)
        )
    ''')

    conn.commit()
    conn.close()
    print("Database created successfully!")


