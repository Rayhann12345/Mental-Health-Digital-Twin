"""
attention_filter_v2.py

Part 1 of 4

Stage 1
--------

Current Effect Determination

Stage 2
--------

Initial Priority Assignment

This module performs NO reinforcement,
ranking,
selection,
behavioural interpretation,
or assessment generation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

from assessment_context import (
    AssessmentContext,
    ParameterContext
)

# ==========================================================
# ENUMS
# ==========================================================

class ParameterPolarity(Enum):

    POSITIVE = "positive"

    NEGATIVE = "negative"

    STABLE = "stable"


class CurrentEffect(Enum):

    BENEFICIAL = "Beneficial"

    HARMFUL = "Harmful"

    NEUTRAL = "Neutral"


class BehaviourState(Enum):

    EMERGING = "Emerging"

    PERSISTENT = "Persistent"

    RESOLVING = "Resolving"

    STABLE = "Stable"


class Severity(Enum):

    NONE = "None"

    LOW = "Low"

    MODERATE = "Moderate"

    HIGH = "High"


class PriorityTier(Enum):

    TIER_1 = 1

    TIER_2 = 2

    TIER_3 = 3

    TIER_4 = 4

    TIER_5 = 5


# ==========================================================
# OUTPUT MODEL
# ==========================================================

@dataclass
class PrioritizedFinding:

    parameter_name: str

    polarity: ParameterPolarity

    current_effect: CurrentEffect

    severity: Severity

    behavioural_state: BehaviourState

    priority_tier: PriorityTier

    reinforcement_score: float = 0.0

    journal_support: int = 0

    related_support: int = 0

    previous_support: bool = False

    rationale: List[str] = field(default_factory=list)

    related_parameters: List[str] = field(default_factory=list)

    selected: bool = False


# ==========================================================
# CURRENT EFFECT ENGINE
# ==========================================================

class CurrentEffectEngine:

    """
    Constitution Rule 1

    Current Effect is determined only from

        Parameter Polarity
        +
        Anomaly Direction
    """

    @staticmethod
    def determine(

        polarity: ParameterPolarity,

        direction: str

    ) -> CurrentEffect:

        direction = direction.lower()

        if polarity == ParameterPolarity.STABLE:

            return CurrentEffect.NEUTRAL

        if polarity == ParameterPolarity.POSITIVE:

            if direction == "increasing":

                return CurrentEffect.BENEFICIAL

            return CurrentEffect.HARMFUL

        if polarity == ParameterPolarity.NEGATIVE:

            if direction == "decreasing":

                return CurrentEffect.BENEFICIAL

            return CurrentEffect.HARMFUL

        return CurrentEffect.NEUTRAL


# ==========================================================
# BASE PRIORITY ENGINE
# ==========================================================

class BasePriorityEngine:

    """
    Assigns the INITIAL Priority Tier.

    This is intentionally conservative.

    Later stages may

        reinforce,
        reorder,
        promote,
        or demote

    findings using behavioural evidence.
    """

    @staticmethod
    def determine(

        effect: CurrentEffect,

        severity: Severity,

        state: BehaviourState

    ) -> PriorityTier:

        #
        # Neutral findings
        #

        if effect == CurrentEffect.NEUTRAL:

            return PriorityTier.TIER_5

        #
        # High Severity
        #

        if severity == Severity.HIGH:

            if state in (

                BehaviourState.PERSISTENT,

                BehaviourState.EMERGING

            ):

                return PriorityTier.TIER_1

            return PriorityTier.TIER_2

        #
        # Moderate Severity
        #

        if severity == Severity.MODERATE:

            if state in (

                BehaviourState.PERSISTENT,

                BehaviourState.EMERGING

            ):

                return PriorityTier.TIER_2

            return PriorityTier.TIER_3

        #
        # Low Severity
        #

        if severity == Severity.LOW:

            if state == BehaviourState.PERSISTENT:

                return PriorityTier.TIER_3

            return PriorityTier.TIER_4

        return PriorityTier.TIER_5


# ==========================================================
# FINDING FACTORY
# ==========================================================

class FindingFactory:

    """
    Converts ParameterContext

            ↓

    PrioritizedFinding

    No behavioural reinforcement occurs here.
    """

    def build(

        self,

        parameter: ParameterContext

    ) -> Optional[PrioritizedFinding]:

        if parameter.anomaly is None:

            return None

        polarity = ParameterPolarity(

            parameter.polarity.lower()

        )

        severity = Severity(

            parameter.anomaly.severity.capitalize()

        )

        state = BehaviourState(

            parameter.anomaly.state.capitalize()

        )

        effect = CurrentEffectEngine.determine(

            polarity,

            parameter.anomaly.direction

        )

        tier = BasePriorityEngine.determine(

            effect,

            severity,

            state

        )

        parameter.current_effect = effect.value

        parameter.priority_tier = tier.value

        return PrioritizedFinding(

            parameter_name=parameter.parameter_name,

            polarity=polarity,

            current_effect=effect,

            severity=severity,

            behavioural_state=state,

            priority_tier=tier

        )


# ==========================================================
# STAGE 1 BUILDER
# ==========================================================

class StageOneBuilder:

    """
    Executes the deterministic stages

        Current Effect

                ↓

        Base Priority

    for every parameter.

    Returns findings that are ready for
    reinforcement in Part 2.
    """

    def __init__(self):

        self.factory = FindingFactory()

    def build(

        self,

        context: AssessmentContext

    ) -> List[PrioritizedFinding]:

        findings = []

        for parameter in context.parameters.values():

            finding = self.factory.build(parameter)

            if finding is not None:

                findings.append(finding)

        return findings

# ==========================================================
# EVIDENCE MODEL
# ==========================================================

@dataclass
class EvidenceBundle:
    """
    Evidence collected for a finding.

    This class stores behavioural evidence only.

    It does NOT determine priority.
    """

    journal_support: int = 0

    related_support: int = 0

    previous_support: bool = False

    supporting_parameters: List[str] = field(default_factory=list)

    rationale: List[str] = field(default_factory=list)


# ==========================================================
# JOURNAL EVIDENCE
# ==========================================================

class JournalEvidenceCollector:

    """
    Determines how much journal evidence exists
    for a finding.

    It does not interpret journal content.
    """

    def collect(

        self,

        parameter: ParameterContext,

        evidence: EvidenceBundle

    ) -> None:

        journals = parameter.supporting_journals

        evidence.journal_support = len(journals)

        if journals:

            evidence.rationale.append(

                f"{len(journals)} supporting journal entries"

            )


# ==========================================================
# RELATED FINDING EVIDENCE
# ==========================================================

class RelatedFindingCollector:

    """
    Determines which related behavioural findings
    support the current finding.
    """

    def __init__(

        self,

        behavioural_graph

    ):

        self.graph = behavioural_graph

    def collect(

        self,

        finding: PrioritizedFinding,

        context: AssessmentContext,

        evidence: EvidenceBundle

    ) -> None:

        related = self.graph.get_related(

            finding.parameter_name

        )

        supported = []

        for parameter_name in related:

            parameter = context.parameters.get(

                parameter_name

            )

            if parameter is None:

                continue

            if parameter.anomaly is None:

                continue

            supported.append(parameter_name)

        evidence.supporting_parameters = supported

        evidence.related_support = len(supported)

        if supported:

            evidence.rationale.append(

                f"Supported by {len(supported)} related findings"

            )


# ==========================================================
# PREVIOUS ASSESSMENT EVIDENCE
# ==========================================================

class PreviousAssessmentCollector:

    """
    Determines whether this finding has
    appeared in previous behavioural assessments.
    """

    def collect(

        self,

        finding: PrioritizedFinding,

        context: AssessmentContext,

        evidence: EvidenceBundle

    ) -> None:

        for assessment in context.previous_assessments:

            findings = assessment.get(

                "findings",

                []

            )

            if finding.parameter_name in findings:

                evidence.previous_support = True

                evidence.rationale.append(

                    "Previously observed"

                )

                break


# ==========================================================
# EVIDENCE COLLECTOR
# ==========================================================

class EvidenceCollector:

    """
    Collects every deterministic evidence source
    for each finding.

    No ranking occurs here.
    """

    def __init__(

        self,

        behavioural_graph

    ):

        self.journal = JournalEvidenceCollector()

        self.related = RelatedFindingCollector(

            behavioural_graph

        )

        self.previous = PreviousAssessmentCollector()

    def collect(

        self,

        finding: PrioritizedFinding,

        parameter: ParameterContext,

        context: AssessmentContext

    ) -> EvidenceBundle:

        evidence = EvidenceBundle()

        self.journal.collect(

            parameter,

            evidence

        )

        self.related.collect(

            finding,

            context,

            evidence

        )

        self.previous.collect(

            finding,

            context,

            evidence

        )

        return evidence


# ==========================================================
# STAGE TWO BUILDER
# ==========================================================

class StageTwoBuilder:

    """
    Stage Two

        Collect behavioural evidence.

    Returns

        List[
            (PrioritizedFinding,
             EvidenceBundle)
        ]

    Nothing is ranked yet.
    """

    def __init__(

        self,

        behavioural_graph

    ):

        self.collector = EvidenceCollector(

            behavioural_graph

        )

    def build(

        self,

        findings: List[PrioritizedFinding],

        context: AssessmentContext

    ):

        output = []

        for finding in findings:

            parameter = context.parameters[

                finding.parameter_name

            ]

            evidence = self.collector.collect(

                finding,

                parameter,

                context

            )

            output.append(

                (

                    finding,

                    evidence

                )

            )

        return output

# ==========================================================
# RANKING ENGINE
# ==========================================================

class RankingEngine:
    """
    Orders findings using the Constitution.

    This stage NEVER changes a finding's
    Priority Tier.

    It only orders findings within
    the same tier.
    """

    def rank(self, candidates):

        return sorted(

            candidates,

            key=self._sort_key

        )

    def _sort_key(self, candidate):

        finding = candidate.finding
        evidence = candidate.evidence

        state_priority = {

            BehaviourState.PERSISTENT: 0,
            BehaviourState.EMERGING: 1,
            BehaviourState.RESOLVING: 2,
            BehaviourState.STABLE: 3

        }

        return (

            finding.priority_tier.value,

            -evidence.journal_support,

            -evidence.related_support,

            -int(evidence.previous_support),

            state_priority[finding.behavioural_state],

            finding.parameter_name

        )


# ==========================================================
# BEHAVIOURAL BALANCE
# ==========================================================

class BehaviouralBalanceEngine:
    """
    Adds contextual findings when necessary.

    This engine NEVER removes high-priority findings.

    It may include one additional finding
    to improve behavioural balance.
    """

    def apply(self, candidates):

        selected = []

        harmful = []
        beneficial = []
        neutral = []

        for candidate in candidates:

            effect = candidate.finding.current_effect

            if effect == CurrentEffect.HARMFUL:

                harmful.append(candidate)

            elif effect == CurrentEffect.BENEFICIAL:

                beneficial.append(candidate)

            else:

                neutral.append(candidate)

        #
        # If only harmful findings exist,
        # include one beneficial finding.
        #

        if harmful and not beneficial:

            selected.extend(harmful)

            if neutral:

                selected.append(neutral[0])

            return selected

        #
        # If only beneficial findings exist,
        # include one neutral finding.
        #

        if beneficial and not harmful:

            selected.extend(beneficial)

            if neutral:

                selected.append(neutral[0])

            return selected

        #
        # Mixed findings already balanced.
        #

        return candidates


# ==========================================================
# SELECTION ENGINE
# ==========================================================

class SelectionEngine:
    """
    Selects the findings that will be
    forwarded to the Assessment Prompt.

    Trigger Policy determines how many
    findings should be forwarded.
    """

    AUTO_LIMIT = 5

    USER_LIMIT = 10

    def select(

        self,

        candidates,

        user_requested=False

    ):

        limit = (

            self.USER_LIMIT

            if user_requested

            else self.AUTO_LIMIT

        )

        selected = candidates[:limit]

        for candidate in selected:

            candidate.selected = True

        return selected


# ==========================================================
# STAGE THREE BUILDER
# ==========================================================

class StageThreeBuilder:

    """
    Executes

        Ranking
            ↓
        Behavioural Balance
            ↓
        Selection

    Returns the final ordered findings.
    """

    def __init__(self):

        self.ranking = RankingEngine()

        self.balance = BehaviouralBalanceEngine()

        self.selection = SelectionEngine()

    def build(

        self,

        candidates,

        context

    ):

        #
        # Rank
        #

        ranked = self.ranking.rank(

            candidates

        )

        #
        # Behavioural Balance
        #

        balanced = self.balance.apply(

            ranked

        )

        #
        # Final Selection
        #

        selected = self.selection.select(

            balanced,

            context.user_requested

        )

        return selected

