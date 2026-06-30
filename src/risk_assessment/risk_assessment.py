# risk_assessment.py

PST_WEIGHTS = {
    "primary": 3,
    "secondary": 2,
    "tertiary": 1
}

RISK_PATTERNS = {
    "stress_escalation": {
        "primary": ["stress", "anxiety", "optimism", "self_efficacy", "coping_ability"],
        "secondary": ["sentiment_score", "frustration", "social_support", "rumination", "sleep_quality", "resilience"],
        "tertiary": ["task_engagement", "concentration", "self_talk_score"]
    },
    "burnout_like_pattern": {
        "primary": ["emotional_exhaustion", "motivation", "task_engagement", "mental_fatigue", "concentration"],
        "secondary": ["stress", "self_efficacy", "coping_ability", "sentiment_score", "resilience"],
        "tertiary": ["social_support", "optimism", "physical_fatigue"]
    },
    "cognitive_drift": {
        "primary": ["stress", "concentration", "mental_fatigue", "sleep_quality", "task_engagement"],
        "secondary": ["anxiety", "rumination", "coping_ability"],
        "tertiary": ["self_efficacy", "resilience", "social_support"]
    },
    "social_withdrawal": {
        "primary": ["emotional_exhaustion", "social_connectedness", "social_support"],
        "secondary": ["anxiety", "stress", "sadness", "sentiment_score", "coping_ability"],
        "tertiary": ["frustration", "rumination", "sleep_quality", "mental_fatigue"]
    },
    "emotional_distress": {
        "primary": ["sadness", "anxiety", "stress", "self_talk_score"],
        "secondary": ["sentiment_score", "frustration", "coping_ability", "social_support", "rumination"],
        "tertiary": ["optimism", "resilience", "sleep_quality"]
    }
}

EXPECTED_DIRECTIONS = {
    "stress_escalation": {
        "stress": "high", "anxiety": "high", "optimism": "low",
        "self_efficacy": "low", "coping_ability": "low",
        "sentiment_score": "low", "frustration": "high",
        "social_support": "low", "rumination": "high",
        "sleep_quality": "low", "resilience": "low",
        "task_engagement": "low", "concentration": "low",
        "self_talk_score": "low"
    },
    "burnout_like_pattern": {
        "emotional_exhaustion": "high", "motivation": "low",
        "task_engagement": "low", "mental_fatigue": "high",
        "concentration": "low", "stress": "high",
        "self_efficacy": "low", "coping_ability": "low",
        "sentiment_score": "low", "resilience": "low",
        "social_support": "low", "optimism": "low",
        "physical_fatigue": "high"
    },
    "cognitive_drift": {
        "stress": "high", "concentration": "low",
        "mental_fatigue": "high", "sleep_quality": "low",
        "task_engagement": "low", "anxiety": "high",
        "rumination": "high", "coping_ability": "low",
        "self_efficacy": "low", "resilience": "low",
        "social_support": "low"
    },
    "social_withdrawal": {
        "emotional_exhaustion": "high", "social_connectedness": "low",
        "social_support": "low", "anxiety": "high",
        "stress": "high", "sadness": "high",
        "sentiment_score": "low", "coping_ability": "low",
        "frustration": "high", "rumination": "high",
        "sleep_quality": "low", "mental_fatigue": "high"
    },
    "emotional_distress": {
        "sadness": "high", "anxiety": "high", "stress": "high",
        "self_talk_score": "low", "sentiment_score": "low",
        "frustration": "high", "coping_ability": "low",
        "social_support": "low", "rumination": "high",
        "optimism": "low", "resilience": "low",
        "sleep_quality": "low"
    }
}


def calculate_percentage(count, total):
    if total == 0:
        return 0

    return (count / total) * 100


def format_parameter_name(parameter):
    return parameter.replace("_", " ").title()


def generate_indicator_sentence(parameter, direction):
    parameter_name = format_parameter_name(parameter)

    if direction == "high":
        return f"{parameter_name} has been abnormally high."

    if direction == "low":
        return f"{parameter_name} has been unusually low."

    return f"{parameter_name} has shown an unusual deviation."


def classify_parameter(issue_name, parameter, actual_direction):
    expected_direction = EXPECTED_DIRECTIONS[issue_name].get(parameter)

    if expected_direction is None:
        return "neutral"

    if actual_direction == expected_direction:
        return "supporting"

    return "opposing"


def calculate_issue_score(issue_name, anomaly_data):
    issue = RISK_PATTERNS[issue_name]

    supporting_parameters = {
        "primary": [],
        "secondary": [],
        "tertiary": []
    }

    opposing_parameters = {
        "primary": [],
        "secondary": [],
        "tertiary": []
    }

    for level in ["primary", "secondary", "tertiary"]:
        for parameter in issue[level]:
            if parameter in anomaly_data:
                actual_direction = anomaly_data[parameter]

                classification = classify_parameter(
                    issue_name,
                    parameter,
                    actual_direction
                )

                if classification == "supporting":
                    supporting_parameters[level].append(parameter)

                elif classification == "opposing":
                    opposing_parameters[level].append(parameter)

    supporting_score = 0
    opposing_score = 0
    issue_details = {}

    for level in ["primary", "secondary", "tertiary"]:
        total_parameters = len(issue[level])

        supporting_count = len(supporting_parameters[level])
        opposing_count = len(opposing_parameters[level])

        supporting_percent = calculate_percentage(
            supporting_count,
            total_parameters
        )

        opposing_percent = calculate_percentage(
            opposing_count,
            total_parameters
        )

        supporting_score += supporting_percent * PST_WEIGHTS[level]
        opposing_score += opposing_percent * PST_WEIGHTS[level]

        issue_details[level] = {
            "supporting_percent": round(supporting_percent, 2),
            "opposing_percent": round(opposing_percent, 2),
            "supporting_parameters": supporting_parameters[level],
            "opposing_parameters": opposing_parameters[level]
        }

    net_score = supporting_score - opposing_score

    primary_supporting_percent = issue_details["primary"]["supporting_percent"]
    primary_opposing_percent = issue_details["primary"]["opposing_percent"]
    primary_net_percent = primary_supporting_percent - primary_opposing_percent

    issue_result = {
        "issue": issue_name,
        "net_score": round(net_score, 2),
        "primary_net_percent": round(primary_net_percent, 2),
        "supporting_score": round(supporting_score, 2),
        "opposing_score": round(opposing_score, 2),
        "details": issue_details,
        "core_indicators": supporting_parameters["primary"],
        "supporting_indicators": supporting_parameters["secondary"],
        "opposing_indicators": (
            opposing_parameters["primary"]
            + opposing_parameters["secondary"]
            + opposing_parameters["tertiary"]
        )
    }

    return issue_result


def get_probability_message(issue_title, risk_score, primary_net_percent):
    if primary_net_percent >= 50 or risk_score >= 350:
        return f"{issue_title} is extremely probable."

    elif risk_score >= 300:
        return f"{issue_title} is highly probable."

    elif risk_score >= 250:
        return f"{issue_title} is quite evident."

    elif risk_score >= 200:
        return f"{issue_title} is probable."

    return None


def get_observation_message(anomaly_data):
    observation_messages = []

    for parameter in anomaly_data:
        direction = anomaly_data[parameter]
        sentence = generate_indicator_sentence(parameter, direction)
        observation_messages.append(sentence)

    return "\n".join(observation_messages)


def assess_risk(anomaly_data):
    if not anomaly_data:
        return {
            "message": "No significant anomalies were detected.",
            "selected_issue": None
        }

    highest_score = -1
    best_issue = None

    for issue_name in RISK_PATTERNS:
        issue_result = calculate_issue_score(
            issue_name,
            anomaly_data
        )

        current_score = issue_result["net_score"]

        if current_score > highest_score:
            highest_score = current_score
            best_issue = issue_result

    if best_issue is None:
        return {
            "message": get_observation_message(anomaly_data),
            "selected_issue": None
        }

    if len(anomaly_data) == 1:
        return {
            "message": get_observation_message(anomaly_data),
            "selected_issue": None
        }

    issue_title = best_issue["issue"].replace("_", " ").title()

    probability_message = get_probability_message(
        issue_title,
        best_issue["net_score"],
        best_issue["primary_net_percent"]
    )

    if probability_message is None:
        return {
            "message": get_observation_message(anomaly_data),
            "selected_issue": None
        }

    output = []

    output.append(probability_message)
    output.append("")

    if best_issue["core_indicators"]:
        output.append("Core Indicators:")

        for parameter in best_issue["core_indicators"]:
            output.append(
                "- " + generate_indicator_sentence(
                    parameter,
                    anomaly_data[parameter]
                )
            )

    if best_issue["supporting_indicators"]:
        output.append("")
        output.append("Supporting Indicators:")

        for parameter in best_issue["supporting_indicators"]:
            output.append(
                "- " + generate_indicator_sentence(
                    parameter,
                    anomaly_data[parameter]
                )
            )

    if best_issue["opposing_indicators"]:
        output.append("")
        output.append("Opposing Indicators:")

        for parameter in best_issue["opposing_indicators"]:
            output.append(
                "- " + generate_indicator_sentence(
                    parameter,
                    anomaly_data[parameter]
                )
            )

    return {
        "message": "\n".join(output),
        "selected_issue": best_issue
    }