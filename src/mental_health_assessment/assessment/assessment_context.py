"""
assessment_context.py

Creates the AssessmentContext object used throughout the
deterministic assessment pipeline.

Responsibilities
----------------
• Load journal entries
• Load baseline values
• Load parameter history
• Load anomaly information
• Load previous assessments

This module performs NO behavioural reasoning.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any

from data_module import query
from anomaly_module.anomaly_detector import AnomalyDetector


# ==========================================================
# DATA CLASSES
# ==========================================================

@dataclass
class AnomalyContext:
    """
    Raw anomaly output from the anomaly module.

    behavioural_recommendation is stored for completeness
    but is NOT used by the deterministic assessment engine.
    """

    parameter_name: str

    severity: str

    direction: str

    state: str

    behavioural_recommendation: Optional[str] = None


@dataclass
class ParameterContext:
    """
    Information about one behavioural parameter.
    """

    parameter_name: str

    baseline: float

    polarity: str = ""

    history: List[float] = field(default_factory=list)

    anomaly: Optional[AnomalyContext] = None

    # Filled later by Attention Filters

    classification: Optional[str] = None

    deviation: Optional[float] = None

    current_effect: Optional[str] = None

    priority_tier: Optional[int] = None

    supporting_journals: List[int] = field(default_factory=list)


@dataclass
class AssessmentContext:

    user_id: int

    user_requested: bool = False

    baselines: Dict[str, float] = field(default_factory=dict)

    parameters: Dict[str, ParameterContext] = field(default_factory=dict)

    journal_entries: List[dict] = field(default_factory=list)

    previous_assessments: List[dict] = field(default_factory=list)


# ==========================================================
# CONTEXT BUILDER
# ==========================================================

class AssessmentContextBuilder:

    def __init__(self):

        self.detector = AnomalyDetector()

    def build(
        self,
        user_id: int,
        user_requested: bool = False
    ) -> AssessmentContext:

        context = AssessmentContext(

            user_id=user_id,

            user_requested=user_requested

        )

        # --------------------------------------------------
        # Baselines
        # --------------------------------------------------

        baselines = query.get_all_baselines(user_id)

        if baselines is None:
            baselines = {}

        context.baselines = baselines

        # --------------------------------------------------
        # Journal Entries
        #
        # Replace with teammate function.
        # --------------------------------------------------

        if hasattr(query, "get_all_entries"):

            context.journal_entries = query.get_all_entries(user_id)

        # --------------------------------------------------
        # Previous Assessments
        #
        # Future module
        # --------------------------------------------------

        if hasattr(query, "get_previous_assessments"):

            context.previous_assessments = (
                query.get_previous_assessments(user_id)
            )

        # --------------------------------------------------
        # Build Parameter Contexts
        # --------------------------------------------------

        for parameter_name, baseline in baselines.items():

            history = []

            if hasattr(query, "get_parameter_history"):

                history = query.get_parameter_history(

                    user_id,

                    parameter_name

                )

            parameter_context = ParameterContext(

                parameter_name=parameter_name,

                baseline=baseline,

                history=history

            )

            # ----------------------------------------------
            # Raw anomaly output
            # ----------------------------------------------

            try:

                anomaly_output = self.detector.evaluate_parameter(

                    user_id,

                    parameter_name

                )

                if anomaly_output is not None:

                    parameter_context.anomaly = AnomalyContext(

                        parameter_name=anomaly_output["parameter_name"],

                        severity=anomaly_output["severity"],

                        direction=anomaly_output["direction"],

                        state=anomaly_output["state"],

                        behavioural_recommendation=
                            anomaly_output.get(
                                "behavioural_recommendation"
                            )

                    )

            except Exception:

                #
                # If anomaly cannot be retrieved,
                # continue gracefully.
                #

                parameter_context.anomaly = None

            context.parameters[parameter_name] = parameter_context

        return context