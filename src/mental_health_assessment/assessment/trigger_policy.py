"""
trigger_policy.py

Determines whether a V1 or V2 behavioural assessment should be generated.

The policy is based on:

V1 period
---------
• Entries 1–19:
    No assessment.

• Entry 20:
    Forced V1 assessment.

• Entries 21–26:
    V1 assessment only when requested by the user.

V2 period
---------
• Entry 27 onward:
    V1 ends permanently and V2 becomes active.

• A user-requested V2 assessment is always generated.

• An automatic V2 assessment is generated when:
    - at least one anomaly has High severity, or
    - at least two anomalies have Moderate severity.

This module only decides whether an assessment should run.
It performs no behavioural interpretation.
"""

from dataclasses import dataclass
from typing import Optional

from .assessment_context import AssessmentContext


# ==========================================================
# CONFIGURATION
# ==========================================================

V1_FORCED_ENTRY = 20
V2_START_ENTRY = 27

HIGH_SEVERITY_REQUIRED = 1
MODERATE_SEVERITY_REQUIRED = 2


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
    Applies the deterministic V1 and V2 triggering rules.
    """

    def evaluate(
        self,
        context: AssessmentContext
    ) -> TriggerDecision:
        """
        Decide whether an assessment should be generated.

        Parameters
        ----------
        context:
            AssessmentContext containing journal entries,
            anomaly outputs and the user-request flag.

        Returns
        -------
        TriggerDecision
            The assessment version, trigger type and reason.
        """

        entry_count = len(context.journal_entries)

        # --------------------------------------------------
        # BEFORE V1
        # Entries 1–19
        # --------------------------------------------------

        if entry_count < V1_FORCED_ENTRY:
            return TriggerDecision(
                should_generate=False,
                trigger_reason="baseline_period_incomplete",
                entry_count=entry_count
            )

        # --------------------------------------------------
        # ENTRY 20
        # Forced first V1 assessment
        # --------------------------------------------------

        if entry_count == V1_FORCED_ENTRY:
            return TriggerDecision(
                should_generate=True,
                assessment_version="v1",
                assessment_type="automatic",
                trigger_reason="forced_initial_v1_assessment",
                entry_count=entry_count
            )

        # --------------------------------------------------
        # V1 USER-REQUEST PERIOD
        # Entries 21–26
        # --------------------------------------------------

        if V1_FORCED_ENTRY < entry_count < V2_START_ENTRY:

            if context.user_requested:
                return TriggerDecision(
                    should_generate=True,
                    assessment_version="v1",
                    assessment_type="user_requested",
                    trigger_reason="v1_manual_request",
                    entry_count=entry_count
                )

            return TriggerDecision(
                should_generate=False,
                assessment_version="v1",
                trigger_reason="v1_waiting_for_user_request",
                entry_count=entry_count
            )

        # --------------------------------------------------
        # V2 PERIOD
        # Entry 27 onward
        # --------------------------------------------------

        # User requests always produce a V2 assessment.
        if context.user_requested:
            high_count, moderate_count = (
                self._count_relevant_anomaly_severities(context)
            )

            return TriggerDecision(
                should_generate=True,
                assessment_version="v2",
                assessment_type="user_requested",
                trigger_reason="v2_manual_request",
                entry_count=entry_count,
                high_anomaly_count=high_count,
                moderate_anomaly_count=moderate_count
            )

        # Automatic V2 triggering depends on anomaly severity.
        high_count, moderate_count = (
            self._count_relevant_anomaly_severities(context)
        )

        if high_count >= HIGH_SEVERITY_REQUIRED:
            return TriggerDecision(
                should_generate=True,
                assessment_version="v2",
                assessment_type="automatic",
                trigger_reason="high_severity_anomaly_detected",
                entry_count=entry_count,
                high_anomaly_count=high_count,
                moderate_anomaly_count=moderate_count
            )

        if moderate_count >= MODERATE_SEVERITY_REQUIRED:
            return TriggerDecision(
                should_generate=True,
                assessment_version="v2",
                assessment_type="automatic",
                trigger_reason="multiple_moderate_anomalies_detected",
                entry_count=entry_count,
                high_anomaly_count=high_count,
                moderate_anomaly_count=moderate_count
            )

        return TriggerDecision(
            should_generate=False,
            assessment_version="v2",
            trigger_reason="v2_automatic_conditions_not_met",
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

        Only the anomaly fields stored in each ParameterContext are
        examined. Behavioural recommendations from the anomaly module
        are ignored.
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