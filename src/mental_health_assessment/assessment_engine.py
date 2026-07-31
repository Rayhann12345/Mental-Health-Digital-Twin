"""
assessment.py

Top-level orchestration for the Mental Health
Assessment Framework.
"""

from .assessment.assessment_context import AssessmentContextBuilder
from .assessment.trigger_policy import TriggerPolicy
from .assessment.attention_filter_v1 import AttentionFilterV1

from .llm.m1 import M1Assessment
from .llm.m2_attention import M2AttentionFilter
from .llm.m2_assessment import M2Assessment


class AssessmentEngine:

    """
    Coordinates the entire assessment pipeline.
    """

    def __init__(self):

        self.context_builder = AssessmentContextBuilder()

        self.trigger_policy = TriggerPolicy()

        self.v1_filter = AttentionFilterV1()

        self.m1 = M1Assessment()

        self.m2_attention = M2AttentionFilter()

        self.m2_assessment = M2Assessment()

    def evaluate(

        self,

        user_id: int,

        version: str = "v2",

        user_requested: bool = False

    ):

        #
        # Step 1
        # Build Assessment Context
        #

        context = self.context_builder.build(

            user_id=user_id,

            user_requested=user_requested

        )

        #
        # Step 2
        # Trigger Policy
        #

        trigger_output = self.trigger_policy.evaluate(

            context

        )

        #
        # Trigger Policy decides
        # whether assessment should happen.
        #

        if not trigger_output.should_generate:

            return {

                "assessment_generated": False,

                "reason": trigger_output

            }

        #
        # -------------------------------
        # Version 1
        # -------------------------------
        #

        if trigger_output.assessment_version == "v1":

            attention_output = self.v1_filter.filter(

                context

            )

            return self.m1.generate(

                context=context,

                trigger_output=trigger_output,

                attention_output=attention_output

            )

        #
        # -------------------------------
        # Version 2
        # -------------------------------
        #

        if trigger_output.assessment_version == "v2":

            attention_output = self.m2_attention.generate(

                context=context,

                trigger_output=trigger_output

            )

            return self.m2_assessment.generate(

                context=context,

                trigger_output=trigger_output,

                attention_output=attention_output

            )

        raise ValueError(

            f"Unknown assessment version returned by Trigger Policy: "
            f"{trigger_output.assessment_version}"

        )


if __name__ == "__main__":

    engine = AssessmentEngine()

    result = engine.evaluate(

        user_id=1,

        version="v2",

        user_requested=False

    )

    print(result)