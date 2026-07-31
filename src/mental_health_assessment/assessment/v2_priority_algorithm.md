# V2 Priority Engine Specification

---

# Purpose

This document defines the deterministic software algorithm used to implement the behavioural prioritisation principles described in **V2 Attention Filter.md**.

Unlike the V2 Attention Filter Constitution, which describes behavioural principles, this specification defines the exact sequence of deterministic operations performed by the software.

The output of this algorithm is an ordered collection of behavioural findings suitable for the V2 Assessment Prompt.

The algorithm performs prioritisation only.

It must never:

- infer behavioural causes,
- generate psychological themes,
- produce recommendations,
- construct narrative assessments.

Those responsibilities remain exclusively with the V2 Assessment Prompt.

---

# Required Inputs

The Priority Engine receives an AssessmentContext containing:

For every behavioural parameter:

- Parameter Name
- Parameter Polarity
- Current Baseline
- Anomaly Direction
- Anomaly Severity
- Behavioural State
- Supporting Journal Entries
- Previous Assessments (optional)

Stable parameters may also be available.

---

# Overall Pipeline

The Priority Engine shall execute the following sequence.

```
Parameter
      │
      ▼
Determine Current Effect
      │
      ▼
Assign Initial Priority Tier
      │
      ▼
Calculate Reinforcement Score
      │
      ▼
Rank Findings Within Each Tier
      │
      ▼
Apply Behavioural Balance
      │
      ▼
Select Findings
      │
      ▼
Return Ordered Findings
```

Each stage is deterministic.

---

# Stage 1 — Determine Current Effect

The first operation is to determine the behavioural effect represented by the anomaly.

Current Effect is determined solely by:

- Parameter Polarity
- Anomaly Direction

The following lookup table shall always be used.

| Polarity | Direction | Current Effect |
|----------|-----------|----------------|
| Positive | Increasing | Beneficial |
| Positive | Decreasing | Harmful |
| Negative | Increasing | Harmful |
| Negative | Decreasing | Beneficial |

Stable parameters have

Current Effect = Neutral

Current Effect must always be calculated before any prioritisation.

---

# Stage 2 — Initial Priority Tier

After determining Current Effect, assign an initial Priority Tier.

The representative Priority Reference Table in the V2 Attention Filter shall be converted into an internal deterministic lookup table.

The lookup key is

```
(Current Effect,
 Severity,
 Behavioural State)
```

The output is

```
Priority Tier
```

The lookup table is authoritative.

Subsequent stages may reorder findings **within the same tier** but must not change the assigned tier.

---

# Stage 3 — Reinforcement Score

Each finding receives a Reinforcement Score.

The Reinforcement Score is used only to rank findings inside the same Priority Tier.

It must never promote or demote findings across tiers.

The score is calculated from the following evidence sources.

---

## 3.1 Journal Support

Each supporting journal contributes evidence.

Journal relevance is determined by the Journal Retrieval module.

More relevant journal evidence increases the Reinforcement Score.

---

## 3.2 Related Behavioural Findings

Behavioural relationships are defined inside

behavioural_graph.py

Examples

Stress

supports

Sleep Quality

Fatigue

Anxiety

Optimism

supports

Motivation

Resilience

Hopefulness

Each related finding increases confidence that the behavioural pattern is genuine.

---

## 3.3 Previous Assessment Support

If the same behavioural finding has appeared in previous assessments, reinforcement increases.

This reflects behavioural consistency across time.

---

## 3.4 Stable Supporting Parameters

Stable parameters do not receive reinforcement.

Instead, they may later be selected to improve behavioural balance.

---

# Stage 4 — Within-Tier Ranking

Findings inside the same Priority Tier shall be sorted using the following order.

1. Greater Reinforcement Score
2. Greater Severity
3. Persistent
4. Emerging
5. Resolving
6. Journal Support
7. Alphabetical Parameter Name

No finding may move into another Priority Tier.

---

# Stage 5 — Behavioural Balance

After ranking is complete, evaluate the behavioural balance of the selected findings.

Examples:

Only harmful findings selected

↓

Optionally include one behaviourally meaningful beneficial or stable finding.

Only beneficial findings selected

↓

Optionally include one relevant harmful finding.

Balance must improve behavioural completeness.

It must never replace higher-priority findings.

---

# Stage 6 — Selection

The Trigger Policy determines whether the assessment is

Automatic

or

User Requested.

The Priority Engine returns findings in ranked order.

The Trigger Policy decides how many findings to forward.

Example

Automatic

Top N findings

User Requested

Top M findings

The Priority Engine itself does not decide N or M.

---

# Output

Each returned finding contains

- Parameter Name
- Current Effect
- Severity
- Behavioural State
- Priority Tier
- Reinforcement Score
- Supporting Journal Count

Optional

- Related Findings
- Stable Context Indicator

The findings are already ordered.

No further prioritisation should occur.

---

# Responsibilities

The Priority Engine

✓ Determines Current Effect

✓ Assigns Priority Tier

✓ Calculates Reinforcement

✓ Ranks Findings

✓ Maintains Behavioural Balance

✓ Returns Ordered Findings

The Priority Engine must never

✗ Generate behavioural themes

✗ Explain behavioural causes

✗ Produce recommendations

✗ Generate assessments

✗ Modify anomaly outputs

✗ Recalculate severity

✗ Recalculate behavioural state

Those responsibilities belong to other components of the Mental Health Assessment Framework.
