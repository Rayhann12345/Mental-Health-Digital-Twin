import sys
sys.path.insert(0, r'C:\Users\ritvi\Documents\mental_health_twin')

from data_module import create_database, add_user, add_entry, get_baseline, get_all_baselines
from anomaly_module import load_user_data, get_model_prediction, evaluate_anomalies

# Setup
create_database()
user_id = add_user("Ritvick", "demo@test.com")

print("\n--- ADDING ENTRIES OVER TIME ---\n")

# Entry 1 - A week ago, very stressed
print("Entry 1 - User is having a very bad week (7 days ago)")
add_entry(user_id=user_id, journal_text="Terrible week, overwhelmed with everything.",
    sentiment_score=-0.8, stress=9, anxiety=8, sadness=7, frustration=8,
    emotional_exhaustion=9, optimism=2, motivation=2, task_engagement=2,
    social_connectedness=3, social_support=3, self_efficacy=2, coping_ability=2,
    resilience=2, concentration=2, mental_fatigue=9, rumination=8,
    self_talk_score=2, sleep_quality=2, sleep_duration=4, physical_fatigue=8,
    cognitive_functioning=2)

# Entry 2 - A few days ago, recovering
print("\nEntry 2 - User is recovering (3 days ago)")
add_entry(user_id=user_id, journal_text="Feeling a bit better today, managed to sleep.",
    sentiment_score=0.1, stress=5, anxiety=5, sadness=4, frustration=4,
    emotional_exhaustion=5, optimism=5, motivation=5, task_engagement=5,
    social_connectedness=5, social_support=5, self_efficacy=5, coping_ability=5,
    resilience=5, concentration=5, mental_fatigue=5, rumination=4,
    self_talk_score=5, sleep_quality=6, sleep_duration=7, physical_fatigue=5,
    cognitive_functioning=5)

# Entry 3 - Today, doing well
print("\nEntry 3 - User is doing well today")
add_entry(user_id=user_id, journal_text="Great day! Feeling motivated and happy.",
    sentiment_score=0.8, stress=2, anxiety=2, sadness=1, frustration=1,
    emotional_exhaustion=2, optimism=9, motivation=9, task_engagement=8,
    social_connectedness=8, social_support=8, self_efficacy=8, coping_ability=8,
    resilience=8, concentration=8, mental_fatigue=2, rumination=1,
    self_talk_score=8, sleep_quality=9, sleep_duration=8, physical_fatigue=2,
    cognitive_functioning=8)

print("\n--- PERSONALIZED BASELINE RESULTS ---\n")
all_baselines = get_all_baselines(user_id)

print(f"Stress baseline:            {round(all_baselines['stress'], 2)}")
print(f"Anxiety baseline:           {round(all_baselines['anxiety'], 2)}")
print(f"Optimism baseline:          {round(all_baselines['optimism'], 2)}")
print(f"Motivation baseline:        {round(all_baselines['motivation'], 2)}")
print(f"Sleep quality baseline:     {round(all_baselines['sleep_quality'], 2)}")
print(f"Sentiment score baseline:   {round(all_baselines['sentiment_score'], 2)}")

print("\n--- WHY IS STRESS BASELINE NOT 9? ---\n")
print("Entry 1 (7 days ago): stress = 9  → LOW weight (old)")
print("Entry 2 (3 days ago): stress = 5  → MEDIUM weight")
print("Entry 3 (today):      stress = 2  → HIGH weight (recent)")
print(f"Exponential decay weighted average → stress baseline = {round(all_baselines['stress'], 2)}")
print("\nRecent improvement is reflected more than the bad week!")

if __name__ == "__main__":
    try:
        TARGET_USER = 1
        
        history, actual, parameter_list, full_df = load_user_data(TARGET_USER)
        predicted = get_model_prediction(history, num_features=len(parameter_list))
        is_anomaly, weight = evaluate_anomalies(actual.numpy(), predicted, parameter_list, full_df)
        
        print(f"Recommended update weight for database baseline: {weight:.2f}")
        
    except Exception as e:
        print(f"Error running pipeline: {e}")
