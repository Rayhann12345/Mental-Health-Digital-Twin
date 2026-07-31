import requests

import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise ValueError("OPENROUTER_API_KEY environment variable not set.")

PROMPT_PATH = "src/mental_health_assessment/v2/prompt.md"
MODEL = "nvidia/nemotron-3-super-120b-a12b:free"

# Read the complete original V2 prompt
with open(PROMPT_PATH, "r", encoding="utf-8") as file:
    runtime_prompt = file.read()

print("Sending the original V2 prompt...")
print("Characters sent:", len(runtime_prompt))

response = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    },
    json={
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": runtime_prompt
            },
            {
                "role": "user",
                "content": (
                    "Confirm that you received and understood the complete "
                    "assessment instructions. Reply in no more than two sentences."
                )
            }
        ],
        "temperature": 0,
        "max_tokens": 150
    },
    timeout=180
)

print("\nHTTP status:", response.status_code)

data = response.json()

if response.status_code != 200:
    print("\nRequest failed:")
    print(data)
else:
    print("\nModel used:", data.get("model"))

    print("\nModel response:")
    print(data["choices"][0]["message"]["content"])

    usage = data.get("usage", {})

    print("\nToken usage:")
    print("Prompt tokens:", usage.get("prompt_tokens"))
    print("Completion tokens:", usage.get("completion_tokens"))
    print("Total tokens:", usage.get("total_tokens"))

for i in range(10):
    print(f"\nRequest {i+1}")

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": runtime_prompt
                },
                {
                    "role": "user",
                    "content": "Reply with only the word OK."
                }
            ],
            "temperature": 0,
            "max_tokens": 5
        }
    )

    print(response.status_code)

    if response.status_code != 200:
        print(response.json())
        break