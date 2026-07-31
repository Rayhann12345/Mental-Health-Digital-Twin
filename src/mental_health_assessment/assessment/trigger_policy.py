"""
trigger_policy.py

Determines whether a V1 or V2 behavioural assessment should be generated.

Simplified policy
-----------------
• Entries 1–19:
    No assessment because the baseline period is incomplete.

• Entries 20–26:
    Always generate a V1 assessment after each new entry.

• Entry 27 onward:
    Always generate a V2 assessment after each new entry.

This module only decides whether an assessment should run.
It performs no behavioural interpretation.
"""

from dataclasses import dataclass
from typing import Optional

from .assessment_context import AssessmentContext


# ==========================================================
# CONFIGURATION
# ==========================================================

V1_START_ENTRY = 20
V2_START_ENTRY = 27


# ==========================================================
# OUTPUT MODEL
# ==========================================================

@dataclass
class TriggerDecision:
    """
    Result returned by the Trigger Policy.
    """

    should_generate: bool

    assessment_version: Optional[str] = None

    assessment_type: Optional[str] = None

    trigger_reason: Optional[str] = None

    entry_count: int = 0

    high_anomaly_count: int = 0

    moderate_anomaly_count: int = 0


# ==========================================================
# TRIGGER POLICY
# ==========================================================

class TriggerPolicy:
    """
    Applies the simplified automatic V1 and V2 triggering rules.
    """

    def evaluate(
        self,
        context: AssessmentContext
    ) -> TriggerDecision:
        """
        Decide whether an assessment should be generated.

        Rules
        -----
        Entries 1–19:
            Do not generate an assessment.

        Entries 20–26:
            Always generate V1.

        Entry 27 onward:
            Always generate V2.
        """

        entry_count = len(context.journal_entries)

        # --------------------------------------------------
        # BASELINE PERIOD
        # Entries 1–19
        # --------------------------------------------------

        if entry_count < V1_START_ENTRY:
            return TriggerDecision(
                should_generate=False,
                assessment_version=None,
                assessment_type=None,
                trigger_reason="baseline_period_incomplete",
                entry_count=entry_count
            )

        # --------------------------------------------------
        # V1 PERIOD
        # Entries 20–26
        # --------------------------------------------------

        if entry_count < V2_START_ENTRY:
            return TriggerDecision(
                should_generate=True,
                assessment_version="v1",
                assessment_type="automatic",
                trigger_reason="automatic_v1_after_entry",
                entry_count=entry_count
            )

        # --------------------------------------------------
        # V2 PERIOD
        # Entry 27 onward
        # --------------------------------------------------

        high_count, moderate_count = (
            self._count_relevant_anomaly_severities(context)
        )

        return TriggerDecision(
            should_generate=True,
            assessment_version="v2",
            assessment_type="automatic",
            trigger_reason="automatic_v2_after_entry",
            entry_count=entry_count,
            high_anomaly_count=high_count,
            moderate_anomaly_count=moderate_count
        )

    # ======================================================
    # INTERNAL HELPERS
    # ======================================================

    @staticmethod
    def _count_relevant_anomaly_severities(
        context: AssessmentContext
    ) -> tuple[int, int]:
        """
        Count High and Moderate anomaly results.

        These counts are no longer used to decide whether V2 runs.
        They are retained only as useful context for the assessment model.
        """

        high_count = 0
        moderate_count = 0

        for parameter_context in context.parameters.values():

            anomaly = parameter_context.anomaly

            if anomaly is None:
                continue

            severity = anomaly.severity.strip().lower()

            if severity == "high":
                high_count += 1

            elif severity == "moderate":
                moderate_count += 1

        return high_count, moderate_count