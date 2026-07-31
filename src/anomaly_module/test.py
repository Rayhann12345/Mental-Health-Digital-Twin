from anomaly_module import AnomalyDetector, load_anomaly_inputs, update_sliding_window, get_user_entry_count


total_days = get_user_entry_count(user_id)

if total_days>=21:
    detector = AnomalyDetector()
    inputs = load_anomaly_inputs(user_id)
    
    for data in inputs:
    
        risk_output, baseline_action, finalized_window = detector.evaluate_parameter(
            param_name=data['param_name'],
            current_value=data['current_value'],
            baseline=data['baseline'],
            std_dev=data['std_dev'],
            historical_window=data['historical_window'],
            max_window_length=data['max_window_length']
        )        
    
        update_sliding_window(user_id=1, param_name=data['param_name'], updated_window=finalized_window)

else:
        days_remaining = 27 - total_days
        print(f"User {user_id} only has {total_days} entries. Skipping Anomaly Detection. "
              f"Needs {days_remaining} more days to establish a stable baseline.")
    





    
