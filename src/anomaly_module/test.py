from anomaly_module import AnomalyDetector, load_anomaly_inputs, update_sliding_window

detector = AnomalyDetector()


inputs = load_anomaly_inputs(user_id=1)

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
    
