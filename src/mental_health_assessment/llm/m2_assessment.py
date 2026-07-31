"""
llm/m2_assessment.py

Gemma wrapper for the Version 2 Behavioural Assessment.
"""

import json

from .gemma import Gemma
from ..framework.prompt_loader import load


class M2Assessment:

    def __init__(self):

        self.model = Gemma()

        self.prompt = load(
            "v2/prompt.md"
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
You are the Version 2 Behavioural Assessment Model for the Mental Health Assessment Framework.

Your responsibility is to produce the final behavioural assessment.

Follow every instruction exactly.

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

Use the Attention Filter output as the primary behavioural evidence.

Use the Assessment Context whenever additional information is required.

Do not invent observations that are unsupported.

Return ONLY the final behavioural assessment.

Do not explain your reasoning.
"""

        return self.model.generate(

            prompt,

            temperature=0.2,

            max_tokens=3000

        )