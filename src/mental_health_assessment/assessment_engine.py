import os
from pathlib import Path

import requests
from dotenv import load_dotenv


# =========================================================
# PATH CONFIGURATION
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

ASSESSMENT_FOLDER = Path(__file__).resolve().parent

FRAMEWORK_FOLDER = ASSESSMENT_FOLDER / "framework"

V2_FOLDER = ASSESSMENT_FOLDER / "v2"


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv(PROJECT_ROOT / ".env")


# =========================================================
# OPENROUTER CONFIGURATION
# =========================================================

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

API_KEY = os.getenv("OPENROUTER_API_KEY")

MODEL = os.getenv(
    "OPENROUTER_MODEL",
    "google/gemma-4-26b-a4b-it:free"
)

if not API_KEY:
    raise RuntimeError(
        "OPENROUTER_API_KEY was not found inside your .env file."
    )


# =========================================================
# DOCUMENT LOADER
# =========================================================

def read_markdown_file(file_path: Path) -> str:
    """
    Reads a markdown file and returns its contents.
    """

    if not file_path.exists():
        raise FileNotFoundError(
            f"Missing file:\n{file_path}"
        )

    return file_path.read_text(
        encoding="utf-8"
    )


def load_document(
    name: str,
    path: Path
) -> str:
    """
    Loads one markdown document while displaying
    connection information.
    """

    print(f"Loading {name}...")

    text = read_markdown_file(path)

    print(
        f"CONNECTED — {len(text):,} characters loaded."
    )

    return text


# =========================================================
# BUILD COMPLETE V2 PIPELINE PROMPT
# =========================================================

def build_pipeline_system_prompt() -> str:
    """
    Creates one large system prompt containing
    every document required by the V2 pipeline.
    """

    assessment_framework = load_document(
        "ASSESSMENT FRAMEWORK",
        FRAMEWORK_FOLDER / "assessment_framework.md"
    )

    trigger_policy = load_document(
        "TRIGGER POLICY",
        FRAMEWORK_FOLDER / "trigger_policy.md"
    )

    attention_filter = load_document(
        "ATTENTION FILTER",
        V2_FOLDER / "attention_filter.md"
    )

    condition_evaluation = load_document(
        "CONDITION EVALUATION",
        FRAMEWORK_FOLDER / "condition_evaluation.md"
    )

    assessment_prompt = load_document(
        "ASSESSMENT PROMPT",
        V2_FOLDER / "prompt.md"
    )

    return f"""
========================================================================
ASSESSMENT FRAMEWORK
========================================================================

{assessment_framework}

========================================================================
TRIGGER POLICY
========================================================================

{trigger_policy}

========================================================================
ATTENTION FILTER
========================================================================

{attention_filter}

========================================================================
CONDITION EVALUATION
========================================================================

{condition_evaluation}

========================================================================
ASSESSMENT PROMPT
========================================================================

{assessment_prompt}
""".strip()

# =========================================================
# BUILD TEST INPUT
# =========================================================

def build_test_input() -> str:
    """
    Fictional behavioural observations used to evaluate
    the complete V2 pipeline.
    """

    return """
This is a controlled software integration test using fictional behavioural data.

Previous Assessment
===================

The previous assessment described a generally balanced behavioural state.
Stress remained within the normal behavioural range, sleep quality was
stable and the user demonstrated a consistently positive outlook.
No significant behavioural concerns were identified.

------------------------------------------------------------

Detected Parameter Changes
==========================

Stress

Parameter Polarity:
Negative

Direction:
Increasing

Severity:
High

Current State:
Persistent Harmful

------------------------------------------------------------

Sleep Quality

Parameter Polarity:
Positive

Direction:
Decreasing

Severity:
Moderate

Current State:
Emerging Harmful

------------------------------------------------------------

Optimism

Parameter Polarity:
Positive

Direction:
Increasing

Severity:
Moderate

Current State:
Persistent Beneficial

------------------------------------------------------------

Emotional Regulation

Parameter Polarity:
Positive

Direction:
Decreasing

Severity:
Low

Current State:
Stable

------------------------------------------------------------

Resilience

Parameter Polarity:
Positive

Direction:
Stable

Severity:
Low

Current State:
Persistent Beneficial

------------------------------------------------------------

Journal Entry
=============

"I've had multiple assignment deadlines this week and I've been
sleeping much later than usual. I still believe everything will
work out eventually, but I feel mentally exhausted by the end
of the day."

Instructions
============

Apply the supplied behavioural pipeline.

Use the Trigger Policy.

Then apply the Attention Filter.

Then perform Condition Evaluation.

Finally generate the behavioural assessment.

Do not reveal intermediate reasoning.

Output only the final behavioural assessment.

Never diagnose a mental-health condition.

Treat the journal only as possible supporting evidence.
""".strip()


# =========================================================
# MODEL REQUEST
# =========================================================

def generate_assessment(
    system_prompt: str,
    user_prompt: str
) -> None:

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/",
        "X-Title": "Mental Health Assessment Test"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        "temperature": 0.2,
        "max_tokens": 500
    }

    print("\nSending request...\n")

    response = requests.post(
        OPENROUTER_URL,
        headers=headers,
        json=payload,
        timeout=180
    )

    print(
        f"HTTP Status: {response.status_code}"
    )

    if response.status_code != 200:
        print("\nRequest failed.\n")
        print(response.text)
        return

    result = response.json()

    print("\n" + "=" * 80)
    print("ASSESSMENT")
    print("=" * 80 + "\n")

    print(
        result["choices"][0]["message"]["content"]
    )

    print("\n" + "=" * 80)
    print("TOKEN USAGE")
    print("=" * 80)

    usage = result.get("usage", {})

    print(
        f"Prompt Tokens     : "
        f"{usage.get('prompt_tokens', 'N/A')}"
    )

    print(
        f"Completion Tokens : "
        f"{usage.get('completion_tokens', 'N/A')}"
    )

    print(
        f"Total Tokens      : "
        f"{usage.get('total_tokens', 'N/A')}"
    )

# =========================================================
# MAIN
# =========================================================

def main():

    print("=" * 80)
    print("MENTAL HEALTH ASSESSMENT")
    print("=" * 80)

    print("\nBuilding complete V2 pipeline prompt...\n")

    system_prompt = build_pipeline_system_prompt()

    print(
        f"System prompt built successfully "
        f"({len(system_prompt):,} characters).\n"
    )

    user_prompt = build_test_input()

    print(
        f"User prompt prepared "
        f"({len(user_prompt):,} characters).\n"
    )

    generate_assessment(
        system_prompt,
        user_prompt
    )


# =========================================================
# ENTRY POINT
# =========================================================

if __name__ == "__main__":
    main()