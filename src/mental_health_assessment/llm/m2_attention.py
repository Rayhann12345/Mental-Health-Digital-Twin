"""
llm/m2_attention.py

Gemma wrapper for the Version 2 Attention Filter.
"""

import json

from .gemma import Gemma
from ..framework.prompt_loader import load


class M2AttentionFilter:

    def __init__(self):

        self.model = Gemma()

        self.constitution = load(
            "v2/attention_filter.md"
        )

    def generate(

        self,

        context,

        trigger_output

    ):

        prompt = f"""
You are the Version 2 Attention Filter for the Mental Health Assessment Framework.

Your ONLY responsibility is to identify and prioritise the behavioural findings that
should receive the model's attention.

DO NOT perform an assessment.

DO NOT make recommendations.

DO NOT diagnose.

Apply the behavioural constitution below exactly.

==================================================
ATTENTION FILTER CONSTITUTION
==================================================

{self.constitution}

==================================================
TRIGGER POLICY OUTPUT
==================================================

{json.dumps(trigger_output, default=lambda o: o.__dict__, indent=4)}

==================================================
ASSESSMENT CONTEXT
==================================================

{json.dumps(context, default=lambda o: o.__dict__, indent=4)}

==================================================

Return ONLY valid JSON.

The JSON must have exactly this format:

{{
    "findings": [
        {{
            "parameter": "...",
            "priority": "...",
            "reason": "...",
            "supporting_evidence": [...]
        }}
    ]
}}

Do not include markdown.

Do not include explanations.

Do not wrap the JSON in ```.

Return ONLY JSON.
"""

        return self.model.generate(

            prompt,

            temperature=0.0,

            max_tokens=700

        )