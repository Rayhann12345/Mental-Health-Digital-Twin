"""
llm/gemma.py

Common OpenRouter wrapper used by all Gemma models.
"""

import os
import requests


class Gemma:

    BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

    def __init__(
        self,
        model="google/gemma-4-26b-a4b-it"
    ):

        self.model = model

        self.api_key = os.getenv("OPENROUTER_API_KEY")

        if self.api_key is None:
            raise ValueError(
                "OPENROUTER_API_KEY environment variable not set."
            )

    def generate(
        self,
        prompt: str,
        temperature: float = 0.2,
        max_tokens: int = 2048
    ) -> str:

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        response = requests.post(
            self.BASE_URL,
            headers=headers,
            json=payload,
            timeout=120
        )

        response.raise_for_status()

        data = response.json()

        return data["choices"][0]["message"]["content"]