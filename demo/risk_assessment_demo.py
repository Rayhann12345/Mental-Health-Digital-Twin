from risk_assessment import assess_risk


test_cases = [
    {
        "name": "Mixed Stress/Cognitive Drift Indicators",
        "input": {
            "stress": "high",
            "anxiety": "high",
            "optimism": "low",
            "coping_ability": "low",
            "rumination": "high",
            "sleep_quality": "low",
            "social_support": "low"
        }
    },
    {
        "name": "Single Anomaly",
        "input": {
            "stress": "high"
        }
    },
    {
        "name": "Opposing Evidence",
        "input": {
            "stress": "high",
            "optimism": "high",
            "coping_ability": "high"
        }
    },
    {
        "name": "Burnout-like Pattern",
        "input": {
            "emotional_exhaustion": "high",
            "motivation": "low",
            "task_engagement": "low",
            "mental_fatigue": "high",
            "concentration": "low",
            "stress": "high"
        }
    },
    {
        "name": "No Anomalies",
        "input": {}
    }
]


for test_case in test_cases:
    print("\n==============================")
    print(test_case["name"])
    print("==============================")

    result = assess_risk(test_case["input"])

    print(result["message"])