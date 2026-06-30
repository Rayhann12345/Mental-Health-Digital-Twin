import numpy as np

def evaluate_anomalies(actual, predicted, parameter_names, full_history_df, threshold=0.15):
    individual_errors = np.abs(actual - predicted)
    
    global_score = np.mean(individual_errors)
    is_anomaly = global_score > threshold
    
    error_report = dict(zip(parameter_names, individual_errors))
    sorted_errors = sorted(error_report.items(), key=lambda x: x[1], reverse=True)
    
    print("\n=== ANOMALY DETECTION REPORT ===")
    print(f"Global Deviation Score: {global_score:.4f}")
    print(f"Status: {'⚠️ ANOMALY DETECTED' if is_anomaly else '✅ NORMAL'}")
    
    if is_anomaly:
        print("\nTop Contributing Parameters:")
        top_culprits = sorted_errors[:3]
        for param, err in top_culprits:
            print(f" • {param} (Deviation: {err:.4f})")
            
        if len(top_culprits) >= 2:
            param1, param2 = top_culprits[0][0], top_culprits[1][0]
            correlation = full_history_df[param1].corr(full_history_df[param2])
            print("\nParameter Connections:")
            print(f" • {param1} and {param2} have a historical correlation of {correlation:.2f}")
    
    if is_anomaly:
        recommended_weight = 0.05
    else:
        recommended_weight = round(1.0 - global_score, 2)
        
    return is_anomaly, recommended_weight