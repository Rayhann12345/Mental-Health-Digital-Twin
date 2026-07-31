from .anomaly_detector import AnomalyDetector
from .data_loader import load_anomaly_inputs, update_sliding_window, get_user_entry_count, save_anomaly_flags
from src.data_module.baseline import calculate_baseline

def run_anomaly_check(user_id):
    try:
        total_days = get_user_entry_count(user_id)
        print(f"[DEBUG] Running anomaly check for User {user_id}. Total days found: {total_days}")
        
        if total_days >= 21:

            calculate_baseline(user_id)
            detector = AnomalyDetector()
            inputs = load_anomaly_inputs(user_id)

            print(f"[DEBUG] Data loaded from database. Parameters found: {len(inputs)}", flush=True)
            if not inputs:
                print("⚠️ WARNING: 'inputs' is empty! The query didn't find the data to evaluate.", flush=True)

            current_entry_flags = {}
            for data in inputs:

                safe_current = float(data['current_value']) if data['current_value'] is not None else 0.0
                safe_baseline = float(data['baseline']) if data['baseline'] is not None else 0.0
                safe_std_dev = float(data['std_dev']) if data['std_dev'] is not None else 0.0

                risk_output, baseline_action, finalized_window = detector.evaluate_parameter(
                    param_name=data['param_name'],
                    current_value=safe_current,
                    baseline=safe_baseline,
                    std_dev=safe_std_dev,
                    historical_window=data['historical_window'],
                    max_window_length=data['max_window_length'],
                    total_days=total_days
                )
                
                update_sliding_window(user_id=user_id, param_name=data['param_name'], updated_window=finalized_window)
                current_entry_flags[data['param_name']] = baseline_action
                
                
                current_state = risk_output.get('State') or risk_output.get('state', 'Unknown')
                current_severity = risk_output.get('Severity') or risk_output.get('severity', 'Unknown')
            
                print(f"📊 [EVALUATED] Param: {data['param_name']} | State: {current_state} | Severity: {current_severity} | Action: {baseline_action}", flush=True)
            if current_entry_flags:
                save_anomaly_flags(user_id, current_entry_flags)
                print(f"💾 [SAVED] Anomaly flags logged to database for next baseline calculation.", flush=True)   

        else:
            days_remaining = 27 - total_days
            print(f"[ANOMALY GATEKEEPER] User {user_id} has {total_days} entries. Needs {days_remaining} more days for baseline.")
            
    except Exception as e:
        print(f"❌ ERROR INSIDE TEST.PY: {str(e)}")





    
