"""
llm/m1.py

Gemma wrapper for Version 1 Assessment.
"""

import json

from .gemma import Gemma
from ..framework.prompt_loader import load


class M1Assessment:

    def __init__(self):

        self.model = Gemma()

        self.prompt = load(

            "v1/prompt.md"

        )

        self.condition = load(

            "framework/condition_evaluation.md"

        )

    def generate(

        self,

        context,

        trigger_output,

        attention_output

    ):

        prompt = f"""
You are the behavioural assessment model for
Version 1 of the Mental Health Assessment Framework.

Follow ALL instructions exactly.

==================================================
CONDITION EVALUATION
==================================================

{self.condition}

==================================================
ASSESSMENT PROMPT
==================================================

{self.prompt}

==================================================
TRIGGER POLICY OUTPUT
==================================================

{json.dumps(trigger_output, default=lambda o: o.__dict__, indent=4)}

==================================================
ATTENTION FILTER OUTPUT
==================================================

{json.dumps(attention_output, indent=4)}

==================================================
ASSESSMENT CONTEXT
==================================================

{json.dumps(context, default=lambda o: o.__dict__, indent=4)}

==================================================

Return ONLY the final assessment.

Do not explain your reasoning.
"""

        return self.model.generate(

            prompt,

            temperature=0.2,

            max_tokens=1500

        )