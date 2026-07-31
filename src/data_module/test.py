import sys
sys.path.insert(0, r'C:\Users\ritvi\Documents\mental_health_twin\Mental-Health-Digital-Twin\src')

from data_module import create_database, add_user, add_entry, get_baseline, get_all_baselines

# Create database
create_database()

# Add a test user
user_id = add_user("Ritvick", "demo@test.com")

print("\n--- ADDING ENTRIES OVER TIME ---\n")

print("Entry 1 - User is having a very bad week (7 days ago)")
add_entry(user_id=user_id, journal_text="Terrible week, overwhelmed with everything.",
    sentiment_score=-0.8, stress=9, anxiety=8, sadness=7, frustration=8,
    emotional_exhaustion=9, optimism=2, motivation=2, task_engagement=2,
    social_connectedness=3, social_support=3, self_efficacy=2, coping_ability=2,
    resilience=2, concentration=2, mental_fatigue=9, rumination=8,
    self_talk_score=2, sleep_quality=2, physical_fatigue=8)

print("\nEntry 2 - User is recovering (3 days ago)")
add_entry(user_id=user_id, journal_text="Feeling a bit better today, managed to sleep.",
    sentiment_score=0.1, stress=5, anxiety=5, sadness=4, frustration=4,
    emotional_exhaustion=5, optimism=5, motivation=5, task_engagement=5,
    social_connectedness=5, social_support=5, self_efficacy=5, coping_ability=5,
    resilience=5, concentration=5, mental_fatigue=5, rumination=4,
    self_talk_score=5, sleep_quality=6, physical_fatigue=5)

print("\nEntry 3 - User is doing well today")
add_entry(user_id=user_id, journal_text="Great day! Feeling motivated and happy.",
    sentiment_score=0.8, stress=2, anxiety=2, sadness=1, frustration=1,
    emotional_exhaustion=2, optimism=9, motivation=9, task_engagement=8,
    social_connectedness=8, social_support=8, self_efficacy=8, coping_ability=8,
    resilience=8, concentration=8, mental_fatigue=2, rumination=1,
    self_talk_score=8, sleep_quality=9, physical_fatigue=2)

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

print("\n--- ENTRY 4: FLAGGING STRESS AS 'ADAPT' (this affects ENTRY 5's weight, not this entry's) ---\n")
add_entry(user_id=user_id, journal_text="Stress spiked again, feels different this time.",
    sentiment_score=-0.2, stress=8, anxiety=6, sadness=5, frustration=6,
    emotional_exhaustion=7, optimism=4, motivation=4, task_engagement=4,
    social_connectedness=5, social_support=5, self_efficacy=4, coping_ability=4,
    resilience=5, concentration=4, mental_fatigue=6, rumination=6,
    self_talk_score=4, sleep_quality=5, physical_fatigue=6,
    anomaly_flags={"stress": "adapt"})

print("\n--- ENTRY 5: THIS entry's weight should be boosted 3x, because ENTRY 4 was flagged 'adapt' ---\n")
add_entry(user_id=user_id, journal_text="Still feeling the effects, stress remains high.",
    sentiment_score=-0.3, stress=8, anxiety=6, sadness=5, frustration=6,
    emotional_exhaustion=7, optimism=4, motivation=4, task_engagement=4,
    social_connectedness=5, social_support=5, self_efficacy=4, coping_ability=4,
    resilience=5, concentration=4, mental_fatigue=6, rumination=6,
    self_talk_score=4, sleep_quality=5, physical_fatigue=6)

all_baselines = get_all_baselines(user_id)
print(f"Stress baseline after Entry 5 (boosted by Entry 4's 'adapt' flag): {round(all_baselines['stress'], 2)}")
print("This should be pulled noticeably closer to 8 than it would without the adapt boost.")