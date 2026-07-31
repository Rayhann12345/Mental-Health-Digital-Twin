# Assessment Framework Reference

Version: 1.0

---

# 1. Purpose

This document serves as the primary reference for the Mental Health Assessment module. It defines the terminology, concepts and interpretation rules used throughout the assessment framework. Every assessment prompt, attention filter and evaluation module should treat this document as the authoritative source when interpreting inputs produced by earlier stages of the pipeline.

The Mental Health Assessment module is **an interpretation module, not an analytical module**. It does not perform numerical calculations or machine learning. Instead, it translates quantitative outputs from previous modules into psychologically meaningful, balanced and human-readable assessments.

The objective of this module is to answer:

> **"Given everything that has already been computed, what does it mean for the user's mental wellbeing?"**

Accordingly, the assessment module should never attempt to recompute values or contradict earlier modules. It should instead explain, synthesize and contextualize the information it receives.

If two instruction documents appear to overlap, later documents should be interpreted as refinements rather than replacements unless they explicitly state otherwise.

---

# 2. Position in the Pipeline

The complete Digital Twin pipeline is:

Journal Entries

↓

Parameter Extraction

↓

Personalized Baseline

↓

Adaptive Anomaly Detection

↓

Mental Health Assessment

↓

Dashboard

Each module has a single responsibility.

---

## Journal Entries

Collect the user's daily reflections and written observations.

These provide qualitative information about the user's experiences, emotions, behaviours and life events.

---

## Parameter Extraction

Transforms journal entries into quantitative psychological parameters.

Examples include:

- Stress
- Anxiety
- Motivation
- Optimism
- Resilience
- Emotional Exhaustion
- Sleep Quality

The assessment module **never extracts these parameters itself.**

---

## Personalized Baseline

Learns what is normal for this specific individual.

Instead of comparing users against universal averages, the system establishes each person's own behavioural baseline.

The assessment module **does not calculate or modify baselines.**

---

## Adaptive Anomaly Detection

Determines whether current parameter values deviate significantly from the personalized baseline.

For each anomaly it provides information such as:

- Direction
- Severity
- State
- Confidence
- Supporting evidence

The assessment module **does not detect anomalies.**

---

## Mental Health Assessment

This module receives outputs from all previous stages and generates a psychologically meaningful interpretation.

Its responsibilities include:

- explaining current mental state
- identifying important behavioural themes
- relating observations to journal evidence
- providing balanced feedback
- offering practical recommendations
- communicating findings in a supportive and understandable manner

---

# 3. Inputs Received

The assessment module may receive any combination of the following inputs depending on the assessment stage.

## From Personalized Baseline

- personalized baseline values
- recent journal entries
- recent parameter values

---

## From Adaptive Anomaly Detection

For every detected anomaly:

- parameter
- severity
- direction
- state

---

# 4. Responsibilities

The assessment module SHOULD:

✓ Explain.

✓ Interpret.

✓ Summarize.

✓ Synthesize.

✓ Provide context.

✓ Connect multiple observations into meaningful behavioural patterns.

✓ Generate psychologically balanced recommendations.

---

The assessment module MUST NOT:

✗ Calculate parameters.

✗ Modify parameter values.

✗ Recalculate baselines.

✗ Detect anomalies.

✗ Modify anomaly severity.

✗ Invent condition scores.

✗ Contradict upstream modules.

---

# 5. Parameter Polarity

Every psychological parameter belongs to one of two categories.

---

## Positive Parameters

Higher values generally indicate healthier functioning.

Examples include:

- Optimism
- Motivation
- Resilience
- Self-Efficacy
- Social Connectedness

Increasing values generally represent improvement.

Decreasing values generally represent deterioration.

---

## Negative Parameters

Higher values generally indicate poorer wellbeing.

Examples include:

- Stress
- Anxiety
- Emotional Exhaustion
- Rumination
- Frustration

Increasing values generally represent deterioration.

Decreasing values generally represent improvement.

---

# 6. Direction

Direction describes **where the current value lies relative to the personalized baseline.**

Direction does **NOT** indicate whether the situation is good or bad.

Direction alone has no emotional meaning.

---

## Positive Direction

Current value is above the personalized baseline.

---

## Negative Direction

Current value is below the personalized baseline.

---

Whether this is desirable depends entirely on the parameter polarity.

---

# 7. Current Effect

Current wellbeing should always be interpreted using both **Parameter Polarity** and **Direction**.

| Parameter Polarity | Direction | Current Effect |
|--------------------|-----------|----------------|
| Positive | Positive | Beneficial |
| Positive | Negative | Harmful |
| Negative | Positive | Harmful |
| Negative | Negative | Beneficial |

This table should always be used when interpreting anomaly direction.

Direction should never be interpreted independently.

---

# 8. Severity

Severity represents the magnitude of the current deviation from the personalized baseline.

It describes **how unusual the current condition is**, not how long it has existed.

Severity levels are ordinal.

Low

Small deviation.

Usually worth monitoring.

Moderate

Meaningful deviation.

Often deserves discussion.

High

Large deviation.

Usually requires prominent attention.

Future versions of the framework may introduce additional levels (e.g. Critical), but assessment logic should remain independent of the exact number of levels.

---

# 9. State

State describes **how the anomaly is evolving over time.**

It does **not** describe whether the anomaly is desirable.

The current framework uses four states.

---

## Emerging

The anomaly is becoming more pronounced.

The deviation from baseline is increasing.

---

## Persistent

The anomaly has remained relatively stable over multiple observations.

It is an established behavioural pattern rather than a temporary fluctuation.

---

## Resolving

The anomaly is moving towards the personalized baseline.

Resolving **does not mean resolved.**

A severe anomaly may still exist while resolving.

---

## Stable

The parameter remains close to the personalized baseline.

Stable parameters are generally not considered anomalous.

However, stable parameters may still be referenced to provide context or emotional balance during an assessment.

---

# 10. Interpreting Resolving Anomalies

Resolving is one of the most important concepts in the framework.

The assessment module must never assume that resolving means healthy.

Instead,

Resolving only indicates that the deviation from baseline is decreasing.

Examples:

High stress

↓

Still well above baseline

↓

But slowly decreasing

↓

"Stress remains elevated, although it appears to be improving."

NOT

"Stress has recovered."

Similarly,

High optimism

↓

Still well above baseline

↓

Beginning to return toward baseline

↓

"Optimism remains noticeably stronger than usual, although the improvement is becoming less pronounced."

NOT

"Optimism has worsened."

The current condition should always be described before describing its trajectory.

---

# 11. Evidence Hierarchy

Every explanation generated by the assessment module should follow the following evidence hierarchy.

## Primary Evidence

Journal entries.

Observed behaviours.

Parameter values.

Baselines.

Anomalies.

Condition scores.

These should always receive the greatest weight.

---

## Secondary Evidence

General psychological knowledge.

Established behavioural science.

Reasonable psychological hypotheses.

These may be used to explain possible causes **only when they do not contradict primary evidence.**

Whenever psychological knowledge is used without direct journal evidence, the language should remain tentative.

Examples:

"may"

"might"

"could"

"appears consistent with"

Avoid presenting inferred causes as confirmed facts.

When Primary Evidence conflicts with general psychological knowledge, Primary Evidence always takes precedence.

---

# 12. Behavioural Theme Synthesis

The goal of the assessment is not to describe individual parameters one after another.

Instead, related parameters should be combined, before individual parameter-level observations are discussed, into coherent behavioural themes whenever appropriate.

For example,

Stress

Mental Fatigue

Sleep Quality

Emotional Exhaustion

may collectively indicate:

"Sustained pressure with insufficient recovery."

Similarly,

Optimism

Resilience

Motivation

may collectively indicate:

"Strong psychological coping despite current challenges."

The assessment should explain the behavioural theme first, followed by the supporting evidence.

However, unrelated parameters should not be artificially grouped together.

When appropriate, the assessment may consult the Condition Evaluation Framework as a reference to determine whether an identified behavioural theme closely aligns with one of the predefined behavioural conditions. The framework should support and refine behavioural interpretation rather than replace it, and conditions should only be referenced when they provide meaningful explanatory value beyond the behavioural theme itself.

---

# 13. Assessment Philosophy

The assessment should be:

Accurate.

Evidence-driven.

Supportive.

Balanced.

Explainable.

The purpose is neither to reassure the user unnecessarily nor to overwhelm them with negative findings.

Whenever genuine positive developments exist, they should be acknowledged.

Whenever meaningful concerns exist, they should be communicated honestly and constructively.

The assessment should resemble the reasoning of a thoughtful mental health professional rather than a statistical report.

Every assessment should ultimately help the user better understand:

- what is happening,
- why it may be happening,
- what appears to be improving,
- what deserves attention,
- and what practical steps may be helpful moving forward.

---

# 14. Guiding Principle

The numerical modules determine **what** has changed.

The Mental Health Assessment module explains **what those changes collectively mean**.