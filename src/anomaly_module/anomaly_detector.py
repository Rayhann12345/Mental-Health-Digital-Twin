import numpy as np

class AnomalyDetector:
    def __init__(self):
        self.std_multiplier = 1.25

    def _get_weights(self, window_length):
        """Generates smooth recency weights scaling linearly from 1.0 to 2.0."""
        if window_length == 0: return np.array([])
        return np.linspace(1.0, 2.0, window_length)

    def _get_deviation_label(self, current_value, baseline, std_dev):

        upper_bound = baseline + (self.std_multiplier * std_dev)
        lower_bound = baseline - (self.std_multiplier * std_dev)
        
        if current_value > upper_bound:
            return '+'
        elif current_value < lower_bound:
            return '-'
        else:
            return '0'

    def evaluate_parameter(self, param_name, current_value, baseline, std_dev, historical_window, max_window_length):

        new_label = self._get_deviation_label(current_value, baseline, std_dev)
        

        current_window = historical_window + [new_label]
        if len(current_window) > max_window_length:
            current_window = current_window[-max_window_length:]
            
        current_length = len(current_window)
        weights = self._get_weights(current_length)
        total_weight = np.sum(weights)
        

        direction_score_raw = 0.0
        deviation_density_raw = 0.0
        

        older_half_dev_weight = 0.0
        newer_half_dev_weight = 0.0
        mid_point = current_length // 2
        
        for i, label in enumerate(current_window):
            w = weights[i]
            if label == '+':
                direction_score_raw += w
                deviation_density_raw += w
                if i < mid_point: older_half_dev_weight += w
                else: newer_half_dev_weight += w
            elif label == '-':
                direction_score_raw -= w
                deviation_density_raw += w
                if i < mid_point: older_half_dev_weight += w
                else: newer_half_dev_weight += w
                

        direction_score = direction_score_raw / total_weight if total_weight > 0 else 0
        deviation_density = deviation_density_raw / total_weight if total_weight > 0 else 0
        
    
        if direction_score > 0.33: direction = "Positive"
        elif direction_score < -0.33: direction = "Negative"
        else: direction = "Neutral"

    
        if deviation_density < 0.33: severity = "Low"
        elif deviation_density <= 0.60: severity = "Moderate"
        else: severity = "High"
        

        recent_is_zero = (current_window[-1] == '0' and (current_length < 2 or current_window[-2] == '0'))
        
        if deviation_density < 0.33:
            state = "Stable"
        elif deviation_density > 0.66 and direction != "Neutral":
            state = f"Persistent {direction}"
        elif direction == "Neutral":
            state = "Mixed"
        else:

            if newer_half_dev_weight >= (2 * older_half_dev_weight) and not recent_is_zero:
                state = f"Emerging {direction}"
            elif older_half_dev_weight >= (2 * newer_half_dev_weight) and recent_is_zero:
                state = f"Resolving {direction}"
            else:

                state = f"Emerging {direction}" if newer_half_dev_weight > older_half_dev_weight else f"Resolving {direction}"

        # Determine Baseline Recommendation
        if state == "Stable":
            baseline_action = "Normal"
        elif "Persistent" in state:
            baseline_action = "Adapt"
        else:
            # Covers Mixed, Emerging, and Resolving
            baseline_action = "Protect"
            

        risk_output = {
            "Parameter": param_name,
            "Direction": direction,
            "Severity": severity,
            "State": state
        }
        
        return risk_output, baseline_action, current_window
