from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from src.anomaly_module.test import run_anomaly_check
from nlp_module import analyze_journal_window
from src.data_module.query import get_db_connection, get_user_id_by_email, get_recent_journals, save_new_entry

app = Flask(__name__)
CORS(app)

@app.route('/api/analyze', methods=['POST'])
def analyze_endpoint():
    try:
        data = request.get_json()
        user_email = data.get('operator')
        new_journal_text = data.get('analyzedText')
        
        if not user_email or not new_journal_text:
            return jsonify({"error": "Missing operator or text"}), 400

        user_id = get_user_id_by_email(user_email)
        past_entries = get_recent_journals(user_id, limit=13) 
        full_entry_window = past_entries + [new_journal_text]

        llm_output = analyze_journal_window(full_entry_window)
        
        if not llm_output:
            return jsonify({"error": "NLP processing failed"}), 500

        numerical_scores = {}
        for param, details in llm_output.items():
            if isinstance(details, dict) and "score" in details:
                numerical_scores[param] = details["score"]
            else:
                numerical_scores[param] = details 

        valid_columns = {
            "sentiment_score", "stress", "anxiety", "sadness", "frustration", 
            "emotional_exhaustion", "optimism", "motivation", "task_engagement", 
            "social_connectedness", "social_support", "self_efficacy", "coping_ability", 
            "resilience", "concentration", "mental_fatigue", "rumination", 
            "self_talk_score", "sleep_quality", "physical_fatigue"
        }
        filtered_scores = {k: v for k, v in numerical_scores.items() if k in valid_columns}
        save_new_entry(user_id, new_journal_text, filtered_scores)

        try:
            run_anomaly_check(user_id)
        except Exception as anomaly_error:
            print(f"Anomaly check failed, but data was saved. Error: {anomaly_error}")


        return jsonify({
            "status": "success",
            "parameters": numerical_scores
        }), 200

    except Exception as e:
        print(f"API Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)
