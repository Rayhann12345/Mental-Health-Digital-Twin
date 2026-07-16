import os
import sqlite3
import pandas as pd
import torch

def load_user_data(target_user_id):
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'mental_health.db')
    
    conn = sqlite3.connect(db_path)
    query = f"SELECT * FROM Entries WHERE user_id = {target_user_id} ORDER BY timestamp ASC"
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    ignored_cols = ['entry_id', 'user_id', 'timestamp', 'journal_text']
    parameter_names = [col for col in df.columns if col not in ignored_cols]
    
    numeric_df = df[parameter_names].astype(float)
    
    if len(numeric_df) < 14:
        raise ValueError(f"Not enough historical data for user {target_user_id}. Need at least 14 rows.")
    
    history_data = numeric_df.iloc[-14:-1].values
    newest_actual = numeric_df.iloc[-1].values
    
    history_tensor = torch.tensor(history_data, dtype=torch.float32).unsqueeze(0)
    newest_tensor = torch.tensor(newest_actual, dtype=torch.float32)
    
    return history_tensor, newest_tensor, parameter_names, numeric_df