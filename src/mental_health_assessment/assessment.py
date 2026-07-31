import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq


# ---------------------------------------------------------
# PATHS
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ASSESSMENT_FOLDER = Path(__file__).resolve().parent

FRAMEWORK_FOLDER = ASSESSMENT_FOLDER / "framework"
V1_FOLDER = ASSESSMENT_FOLDER / "v1"

load_dotenv(PROJECT_ROOT / ".env")


# ---------------------------------------------------------
# FILE READING
# ---------------------------------------------------------

def read_markdown_file(file_path: Path) -> str:
    """
    Read a Markdown file and return its contents.
    """

    if not file_path.exists():
        raise FileNotFoundError(f"Could not find file: {file_path}")

    return file_path.read_text(encoding="utf-8")


def load_document(name: str, path: Path) -> str:
    """
    Load one document and print its character count.
    """

    print(f"Loading {name}...")

    text = read_markdown_file(path)

    print(f"CONNECTED — {len(text)} characters loaded.")

    return text


# ---------------------------------------------------------
# BUILD SYSTEM INSTRUCTIONS
# ---------------------------------------------------------

def build_v1_system_prompt() -> str:
    """
    Build a temporary V1 system prompt using only:
    1. Assessment Framework
    2. V1 Assessment Prompt
    """

    assessment_framework = load_document(
        "ASSESSMENT FRAMEWORK",
        FRAMEWORK_FOLDER / "assessment_framework.md",
    )

    v1_prompt = load_document(
        "V1 ASSESSMENT PROMPT",
        V1_FOLDER / "prompt.md",
    )

    return f"""
============================================================
ASSESSMENT FRAMEWORK
============================================================

{assessment_framework}


============================================================
V1 ASSESSMENT PROMPT
============================================================

{v1_prompt}
""".strip()


# ---------------------------------------------------------
# TEST INPUT
# ---------------------------------------------------------

def build_test_input() -> str:
    """
    Create a small artificial V1 input.

    This is not real user data.
    It exists only to test whether the model follows
    the behavioural interpretation framework.
    """

    return """
This is a controlled software integration test using fictional data.

Assessment Type:
User-requested V1 assessment

Previous Assessment Summary:
The previous assessment indicated a generally balanced behavioural state with
normal stress levels, good sleep quality and a moderately positive outlook.
No significant concerns were identified.

Attention Filter Output:

1. Stress
 Parameter Polarity: Negative
 Current Baseline: 7.8
 Classification: Concerningly Outside the Range
 Direction of Deviation: Above Upper Boundary

2. Sleep Quality
 Parameter Polarity: Positive
 Current Baseline: 2.9
 Classification: Concerningly Outside the Range
 Direction of Deviation: Below Lower Boundary

3. Optimism
 Parameter Polarity: Positive
 Current Baseline: 7.1
 Classification: Beneficially Outside the Range
 Direction of Deviation: Above Upper Boundary

Journal Evidence:
The fictional user reports having several academic deadlines this week
and sleeping later than usual.

Instructions:

- This is a fictional software integration test.
- Produce a behavioural assessment only.
- Do not diagnose any mental-health condition.
- Treat journal evidence only as a possible contributor.
- Do not claim certainty.
- Do not expose internal reasoning.
- Do not use Behavioural Theme names as headings.
- Write naturally, as if speaking to the user.
- Keep the response below 180 words.
""".strip()


# ---------------------------------------------------------
# MAIN MODEL TEST
# ---------------------------------------------------------

def main() -> None:
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        print("FAILED")
        print("GROQ_API_KEY was not found.")
        return

    print("API key found.\n")

    try:
        system_prompt = build_v1_system_prompt()
        test_input = build_test_input()

        print("\nDocuments loaded successfully.")
        print(
            f"System prompt length: {len(system_prompt)} characters"
        )
        print(
            f"Test input length: {len(test_input)} characters"
        )

        client = Groq(api_key=api_key)

        print("\nSending fictional V1 assessment test to Qwen...")

        response = client.chat.completions.create(
            model="qwen/qwen3.6-27b",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": test_input,
                },
            ],
            reasoning_effort="none",
            reasoning_format="hidden",
            temperature=0.3,
            max_completion_tokens=400,
        )

        answer = response.choices[0].message.content

        print("\n" + "=" * 60)
        print("MODEL ASSESSMENT")
        print("=" * 60)
        print(answer)
        print("=" * 60)

    except Exception as error:
        print("\nTEST FAILED")
        print(type(error).__name__)
        print(error)


if __name__ == "__main__":
    main()