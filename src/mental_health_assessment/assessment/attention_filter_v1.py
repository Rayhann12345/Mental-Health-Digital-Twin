"""
attention_filter_v1.py

Implements the deterministic V1 Attention Filter.

Responsibilities
----------------
• Compare every parameter baseline against the V1 reference range.
• Determine behavioural classification.
• Measure deviation.
• Return objective findings only.

This module performs NO behavioural interpretation.
"""

from dataclasses import dataclass
from typing import List

from .assessment_context import AssessmentContext


# ==========================================================
# CONFIGURATION
# ==========================================================

LOWER_BOUND = 3.5
UPPER_BOUND = 6.5


# ==========================================================
# OUTPUT MODEL
# ==========================================================

@dataclass
class V1Finding:

    parameter: str

    polarity: str

    current_baseline: float

    classification: str

    direction: str

    deviation: float


# ==========================================================
# ATTENTION FILTER
# ==========================================================

class AttentionFilterV1:

    def __init__(self):

        pass

    # ------------------------------------------------------

    def filter(
        self,
        context: AssessmentContext
    ) -> List[V1Finding]:

        findings = []

        for parameter_name, parameter in context.parameters.items():

            polarity = parameter.polarity.lower()

            baseline = parameter.baseline

            finding = self._evaluate_parameter(

                parameter_name,

                polarity,

                baseline

            )

            if finding is not None:

                findings.append(finding)

        return findings

    # ------------------------------------------------------

    def _evaluate_parameter(

        self,

        parameter_name: str,

        polarity: str,

        baseline: float

    ) -> V1Finding | None:

        # ----------------------------------------------
        # WITHIN RANGE
        # ----------------------------------------------

        if LOWER_BOUND <= baseline <= UPPER_BOUND:

            return None

        # ----------------------------------------------
        # ABOVE RANGE
        # ----------------------------------------------

        if baseline > UPPER_BOUND:

            deviation = round(
                baseline - UPPER_BOUND,
                2
            )

            direction = "Above Upper Boundary"

            if polarity == "positive":

                classification = (
                    "Beneficially Outside the Range"
                )

            else:

                classification = (
                    "Concerningly Outside the Range"
                )

        # ----------------------------------------------
        # BELOW RANGE
        # ----------------------------------------------

        else:

            deviation = round(
                LOWER_BOUND - baseline,
                2
            )

            direction = "Below Lower Boundary"

            if polarity == "positive":

                classification = (
                    "Concerningly Outside the Range"
                )

            else:

                classification = (
                    "Beneficially Outside the Range"
                )

        return V1Finding(

            parameter=parameter_name,

            polarity=polarity.capitalize(),

            current_baseline=baseline,

            classification=classification,

            direction=direction,

            deviation=deviation

        )