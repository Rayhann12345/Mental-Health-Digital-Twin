# V2 Attention Filter

## Objective

The V2 Attention Filter is responsible for determining **which anomaly findings deserve attention and the relative order in which they should be considered** during a Behavioural Change Assessment.

It does **not** determine whether an anomaly exists. Previous modules have already established this through parameter extraction, personalized baselines, adaptive anomaly detection and condition scoring.

Its sole responsibility is to answer the following questions:

- Which findings are most important?
- Which findings should receive greater attention?
- Which findings provide useful supporting context?
- Which findings can be omitted without significantly affecting the assessment?

The output of this filter is an **ordered collection of prioritized findings**. It does not determine how these findings are combined into behavioural themes or presented in the final assessment. That responsibility belongs to the V2 Assessment Prompt.

---

# Constitution

The following principles govern all prioritization decisions made by the V2 Attention Filter. Unless explicitly stated otherwise, these principles should always be followed.

---

## Rule 1 — Determine the Current Effect Before Anything Else

Every anomaly must first be interpreted using:

- Parameter Polarity
- Anomaly Direction

as defined in the Assessment Framework Reference.

The resulting **Current Effect** determines whether the anomaly currently represents a beneficial or harmful behavioural state.

The anomaly must never be prioritized using direction alone.

For example, an increase in Stress and an increase in Optimism both have a positive direction, but they represent opposite psychological effects due to their different parameter polarities.

Current effect should always be determined before considering severity, persistence or trajectory.

---

## Rule 2 — Severity is the Primary Indicator of Importance

Severity represents the magnitude of deviation from the personalized baseline.

Greater deviations generally indicate more meaningful behavioural changes and therefore deserve greater attention.

However, severity should **not** be treated as the sole determinant of priority.

Other contextual information—including persistence, trajectory, journal evidence and behavioural significance—may justify promoting or demoting findings of similar severity.

Severity provides the starting point for prioritization, not the final decision.

---

## Rule 3 — Persistence Generally Deserves Greater Attention

Persistent anomalies indicate behavioural patterns that have remained consistent across multiple observations.

Emerging anomalies represent newer behavioural changes that may or may not continue.

Given similar severity and current effect:

- Persistent anomalies should generally receive greater attention than emerging anomalies.
- Emerging anomalies should still receive appropriate attention, particularly when they represent the early stages of potentially significant behavioural change.

Persistence reflects behavioural stability, not behavioural severity.

---

## Rule 4 — Correct Interpretation of the Resolving State

The **Resolving** state describes behavioural trajectory.

It does **not** describe behavioural quality.

Resolving simply indicates that an anomaly is moving back toward the personalized baseline.

Whether this represents improvement or weakening depends entirely on the anomaly's current effect.

Therefore, the filter must always determine the current effect before interpreting the resolving state.

Examples:

### Example 1

Stress

- Negative polarity
- Negative direction
- Resolving

Interpretation:

Stress remains below baseline, which is currently beneficial.

However, because it is resolving, this beneficial deviation is becoming smaller as Stress returns toward its normal baseline.

The benefit is weakening.

---

### Example 2

Optimism

- Positive polarity
- Positive direction
- Resolving

Interpretation:

Optimism remains above baseline, which is currently beneficial.

However, because it is resolving, the elevated optimism is gradually returning toward its normal level.

The improvement is fading.

---

### Example 3

Stress

- Negative polarity
- Positive direction
- Resolving

Interpretation:

Stress remains above baseline, which is currently harmful.

However, the anomaly is moving toward baseline.

The harmful state is improving but has not yet disappeared.

---

Consequently:

- Resolving does **not** imply healthy.
- Resolving does **not** imply insignificant.
- Resolving anomalies may still deserve substantial attention when their current effect remains moderate or high.
- A resolving anomaly should never automatically be ranked below every emerging anomaly.

Trajectory modifies the interpretation of an anomaly.

It never replaces its current effect.

---

## Rule 5 — Harmful and Beneficial Findings Both Matter

Behavioural assessments should represent the user's complete behavioural picture rather than focusing exclusively on concerns.

Beneficial anomalies provide valuable evidence regarding coping ability, resilience, recovery and psychological strengths.

Similarly, harmful anomalies identify behavioural difficulties requiring attention.

The filter should therefore prioritize both positive and negative findings whenever they provide meaningful insight into the user's current behavioural state.

High-priority beneficial findings should never be ignored solely because harmful findings exist.

Likewise, beneficial findings should not overshadow severe harmful concerns simply to create an artificially positive assessment.

---

## Rule 6 — Journal Evidence Strengthens Priority

Journal evidence provides behavioural context that numerical values alone cannot capture.

When two anomalies have comparable quantitative importance, stronger support from journal content should increase priority.

Consistent behavioural evidence across multiple journal entries indicates that the anomaly reflects a genuine behavioural pattern rather than an isolated numerical fluctuation.

Journal evidence should strengthen existing findings rather than create new ones.

---

## Rule 7 — Stable Parameters May Be Included for Context

Stable parameters are not behavioural anomalies.

However, they may occasionally provide valuable contextual information.

A stable parameter may be selected when it helps produce a more complete and balanced understanding of the user's behavioural state.

Examples include:

- demonstrating preserved strengths during periods of difficulty,
- showing behavioural stability despite isolated concerns,
- preventing an assessment from presenting an unnecessarily one-sided picture.

Stable parameters should not replace meaningful anomalies.

Their role is supportive rather than primary.

---

## Rule 8 — Maintain Behavioural Balance During Selection

The filter should avoid producing an output that unnecessarily exaggerates either behavioural concern or behavioural wellness.

When only harmful anomalies are selected, the filter may include genuinely relevant stable or beneficial findings that provide important behavioural context.

Similarly, when only beneficial anomalies are selected, the filter may include relevant stable or mildly concerning findings that prevent unrealistic reassurance.

Balance should arise naturally from the evidence.

The objective is not equal representation of positive and negative findings.

The objective is an accurate representation of the user's behavioural state.

---

## Rule 9 — Related Evidence Should Strengthen Priority

Multiple related findings often describe the same underlying behavioural change.

When several anomalies consistently point toward a common behavioural pattern, they collectively provide stronger evidence than isolated findings.

Such mutually supporting findings should generally receive greater priority than independent anomalies of similar severity.

This rule concerns evidence strength only.

The process of combining these findings into behavioural themes is performed later by the V2 Assessment Prompt.

---

## Rule 10 — Avoid Over-Prioritizing Isolated Findings

An anomaly should not receive excessive attention simply because its numerical severity is high.

If surrounding behavioural evidence provides little support for the anomaly, its priority should be considered alongside the broader behavioural picture.

Conversely, several moderate findings consistently pointing toward the same behavioural concern may together deserve greater attention than a single isolated severe anomaly.

Behavioural consistency should always be considered alongside numerical magnitude.

---

## Rule 11 — Prioritization Should Remain Evidence Driven

The filter should prioritize findings using evidence supplied by previous modules.

It should never:

- infer new behavioural conditions,
- assume psychological causes,
- speculate about future outcomes,
- reinterpret numerical outputs.

Its responsibility is prioritization, not behavioural diagnosis.

---

## Rule 12 — Priority Adjustment Principles

When multiple findings receive similar priority, the following considerations should generally be applied in order:

1. Greater severity.
2. Harmful current effect over beneficial current effect.
3. Persistent over Emerging.
4. Stronger journal support.
5. Greater support from related behavioural evidence.
6. Stable parameters should only be preferred when they provide meaningful contextual balance.

These principles are intended to resolve close comparisons.

They should not override the broader Constitution or the ranked reference table.

---

# Filter Output Specification

The output of the V2 Attention Filter should be an ordered collection of prioritized findings together with sufficient supporting information for subsequent assessment generation.

Each selected finding should retain:

- Parameter name
- Current effect (Beneficial or Harmful)
- Severity
- State (Emerging, Persistent or Resolving)
- Relative priority
- Supporting rationale (where applicable)

The filter should not generate behavioural interpretations, behavioural themes, recommendations or narrative explanations.

Its responsibility ends once the findings have been prioritized for use by the V2 Assessment Prompt.

---

# Representative Priority Reference Table

The following table provides representative examples illustrating how the Constitution should be applied when prioritizing behavioural findings.

This table is **illustrative rather than exhaustive**. It is not intended to function as a rigid lookup table. Instead, it demonstrates the intended prioritization behaviour across a variety of commonly encountered scenarios.

When an exact situation is not appear within this table, the V2 Attention Filter should identify the closest comparable scenario and apply the Constitution to determine the appropriate Priority Tier.

The Priority Tiers describe **how much attention a finding deserves**, **not** whether the finding itself is psychologically positive or negative.

Similarly, the examples provided are intended to illustrate representative reasoning patterns rather than define every possible combination of parameter behaviour.

Within each Priority Tier, the order of the rows **does not imply strict ranking**. All representative situations within the same tier should be considered to have broadly comparable behavioural importance unless the Constitution or available behavioural evidence strongly suggests otherwise.

> **Note:** Although **Current Effect** can be derived from the combination of **Polarity** and **Direction**, it is intentionally retained as an explicit column. This reinforces the intended reasoning pipeline, reduces ambiguity and ensures that the V2 Attention Filter explicitly determines the Current Effect before considering Severity, Behavioural State and behavioural priority.

The intended reasoning sequence is therefore:

```
Parameter
    ↓
Polarity
    ↓
Direction
    ↓
Current Effect
    ↓
Severity
    ↓
Behavioural State
    ↓
Priority Tier
```

---

# Priority Tiers

| Priority Tier | Description |
|--------------|-------------|
| **Tier 1 – Highest Attention** | Findings that should receive prominent discussion because they contribute the strongest behavioural insight. |
| **Tier 2 – High Attention** | Important findings that deserve clear discussion but are generally secondary to Tier 1. |
| **Tier 3 – Moderate Attention** | Behaviourally meaningful findings that strengthen understanding of the user's current behavioural state. |
| **Tier 4 – Supporting Attention** | Supporting contextual findings that supplement higher-priority observations. |
| **Tier 5 – Context Only** | Findings that should only be included when they improve behavioural completeness or balance. |

---

# Tier 1 – Highest Attention

## Severe Behavioural Concerns

| Polarity | Direction | Current Effect | Severity | State | Illustrative Finding | Selection Rationale |
|----------|-----------|----------------|----------|-------|----------------------|---------------------|
| Negative | Positive | Harmful | High | Persistent | Stress consistently remains well above baseline. | Severe harmful deviation consistently observed over time requiring prominent discussion. |
| Positive | Negative | Harmful | High | Persistent | Optimism consistently remains well below baseline. | Persistent loss of a major behavioural strength deserves highest attention. |
| Negative | Positive | Harmful | High | Emerging | Stress has recently increased sharply and journal entries consistently support worsening emotional strain. | Rapid deterioration supported by behavioural and journal evidence. |
| Positive | Negative | Harmful | High | Emerging | Motivation has rapidly declined alongside repeated reports of reduced productivity. | Significant emerging deterioration with strong supporting evidence. |
| Negative | Positive | Harmful | High | Resolving | Stress remains substantially above baseline despite gradual improvement. | Although recovering, the current behavioural effect remains significantly harmful. |

---

## Major Behavioural Strengths

| Polarity | Direction | Current Effect | Severity | State | Illustrative Finding | Selection Rationale |
|----------|-----------|----------------|----------|-------|----------------------|---------------------|
| Positive | Positive | Beneficial | High | Persistent | Optimism consistently remains well above baseline. | Major behavioural strength consistently demonstrated over time. |
| Negative | Negative | Beneficial | High | Persistent | Stress consistently remains well below baseline. | Sustained reduction of a major negative behaviour represents an important protective factor. |
| Positive | Positive | Beneficial | High | Emerging | Optimism has increased substantially and journals consistently reflect improved outlook. | Significant positive behavioural improvement deserving strong recognition. |
| Negative | Negative | Beneficial | High | Emerging | Stress has recently reduced considerably following a prolonged difficult period. | Strong behavioural recovery supported by multiple observations. |

---

## Strong Multi-Parameter Evidence

| Polarity | Direction | Current Effect | Severity | State | Illustrative Finding | Selection Rationale |
|----------|-----------|----------------|----------|-------|----------------------|---------------------|
| Mixed | Mixed | Harmful | Moderate | Persistent | Stress, fatigue and sleep quality collectively indicate sustained psychological strain. | Multiple related findings together represent a major behavioural concern despite individually moderate severity. |
| Mixed | Mixed | Beneficial | Moderate | Persistent | Optimism, resilience and motivation consistently improve together over time. | Multiple reinforcing strengths collectively represent significant positive functioning deserving highest attention. |

---

# Tier 2 – High Attention

## Established Behavioural Concerns

| Polarity | Direction | Current Effect | Severity | State | Illustrative Finding | Selection Rationale |
|----------|-----------|----------------|----------|-------|----------------------|---------------------|
| Negative | Positive | Harmful | Moderate | Persistent | Stress remains moderately above baseline across several assessments. | Established behavioural concern requiring discussion. |
| Positive | Negative | Harmful | Moderate | Persistent | Motivation consistently remains moderately below baseline. | Persistent decline of a positive behavioural characteristic. |
| Negative | Positive | Harmful | Moderate | Emerging | Stress is gradually increasing beyond expected variation. | Emerging deterioration that may develop into a larger concern if sustained. |
| Positive | Negative | Harmful | Moderate | Emerging | Social engagement has recently begun declining below baseline. | Developing behavioural concern supported by recent observations. |
| Negative | Positive | Harmful | Moderate | Resolving | Stress remains moderately elevated but continues improving. | Behaviour remains concerning although recovery has begun. |

---

## Significant Positive Behavioural Changes

| Polarity | Direction | Current Effect | Severity | State | Illustrative Finding | Selection Rationale |
|----------|-----------|----------------|----------|-------|----------------------|---------------------|
| Positive | Positive | Beneficial | High | Resolving | Optimism remains above baseline but is gradually returning toward typical levels. | Major behavioural strength remains worthy of discussion despite reducing deviation. |
| Negative | Negative | Beneficial | High | Resolving | Stress remains below baseline while gradually returning toward normal levels. | Significant beneficial state still contributes meaningful behavioural insight. |
| Positive | Positive | Beneficial | Moderate | Persistent | Motivation consistently remains moderately above baseline. | Stable positive behavioural characteristic demonstrated across time. |
| Negative | Negative | Beneficial | Moderate | Persistent | Stress consistently remains moderately below baseline. | Stable reduction in a negative behavioural factor supports overall wellbeing. |
| Positive | Positive | Beneficial | Moderate | Emerging | Confidence has recently begun improving beyond baseline. | Developing positive behavioural trend deserving recognition. |

---

# Tier 3 – Moderate Attention

## Developing Behavioural Patterns

| Polarity | Direction | Current Effect | Severity | State | Illustrative Finding | Selection Rationale |
|----------|-----------|----------------|----------|-------|----------------------|---------------------|
| Positive | Positive | Beneficial | Moderate | Resolving | Motivation remains above baseline but is gradually returning towards its typical level. | Positive behavioural improvement remains relevant although its deviation is reducing. |
| Negative | Positive | Harmful | Low | Persistent | Stress remains slightly above baseline over an extended period. | Mild but consistently observed behavioural concern. |
| Positive | Negative | Harmful | Low | Persistent | Optimism remains slightly below baseline across multiple assessments. | Persistent reduction in a positive behavioural characteristic. |
| Mixed | Mixed | Harmful | Low | Persistent | Mild increases in stress, fatigue and reduced sleep quality collectively indicate sustained pressure. | Multiple low-severity findings together become behaviourally meaningful. |

---

## Behaviourally Important Comparisons

These examples demonstrate that behavioural priority should not be determined solely by severity. Instead, trajectory, behavioural context and supporting evidence may justify comparable prioritisation.

| Polarity | Direction | Current Effect | Severity | State | Illustrative Finding | Selection Rationale |
|----------|-----------|----------------|----------|-------|----------------------|---------------------|
| Negative | Positive | Harmful | High | Resolving | Stress remains elevated but journals consistently demonstrate recovery. | Although severe, improving trajectory may reduce relative attention compared with rapidly worsening concerns. |
| Negative | Positive | Harmful | Moderate | Emerging | Stress has recently begun increasing rapidly with repeated journal evidence. | Emerging deterioration may deserve comparable attention because behavioural trajectory indicates increasing concern. |
| Positive | Positive | Beneficial | High | Persistent | Optimism consistently remains well above baseline despite several unrelated minor concerns. | Major behavioural strengths should not be ignored simply because smaller concerns exist elsewhere. |

---

# Tier 4 – Supporting Attention

## Minor Behavioural Changes

| Polarity | Direction | Current Effect | Severity | State | Illustrative Finding | Selection Rationale |
|----------|-----------|----------------|----------|-------|----------------------|---------------------|
| Negative | Positive | Harmful | Low | Emerging | Stress has recently risen slightly above baseline. | Early behavioural concern requiring continued observation. |
| Positive | Negative | Harmful | Low | Emerging | Motivation has recently declined slightly below baseline. | Small behavioural deterioration that may become significant if sustained. |
| Negative | Positive | Harmful | Low | Resolving | Stress is returning towards baseline after a mild increase. | Minor concern already demonstrating recovery. |
| Positive | Negative | Harmful | Low | Resolving | Confidence is returning towards baseline after a mild decline. | Behavioural concern is already reducing. |
| Positive | Positive | Beneficial | Low | Persistent | Motivation consistently remains slightly above baseline. | Small but stable behavioural strength. |
| Negative | Negative | Beneficial | Low | Persistent | Stress consistently remains slightly below baseline. | Stable reduction of a negative behaviour providing supportive context. |
| Positive | Positive | Beneficial | Low | Emerging | Confidence has recently increased slightly beyond baseline. | Minor positive behavioural improvement. |
| Negative | Negative | Beneficial | Low | Emerging | Stress has recently fallen slightly below baseline. | Early indication of behavioural improvement. |
| Positive | Positive | Beneficial | Low | Resolving | Motivation remains slightly elevated while gradually returning towards baseline. | Positive deviation becoming less pronounced. |
| Negative | Negative | Beneficial | Low | Resolving | Stress remains slightly below baseline while gradually returning towards normal. | Beneficial deviation naturally reducing. |

---

## Behavioural Context

| Polarity | Direction | Current Effect | Severity | State | Illustrative Finding | Selection Rationale |
|----------|-----------|----------------|----------|-------|----------------------|---------------------|
| Stable | Stable | Neutral | None | Stable | Sleep quality has remained consistently normal throughout the observation period. | Stable parameters may provide behavioural balance when they improve representation of the overall behavioural state. |

---

# Tier 5 – Context Only

## Contextual Findings

| Polarity | Direction | Current Effect | Severity | State | Illustrative Finding | Selection Rationale |
|----------|-----------|----------------|----------|-------|----------------------|---------------------|
| Stable | Stable | Neutral | None | Stable | Physical activity has remained unchanged without contributing meaningful behavioural context. | Stable parameter adds little explanatory value. |
| Negative | Positive | Harmful | Low | Emerging | A single isolated increase in stress without supporting evidence. | Behavioural significance is limited due to lack of persistence or supporting evidence. |
| Positive | Negative | Harmful | Low | Emerging | One isolated reduction in optimism unsupported by journals or related findings. | Insufficient evidence for meaningful prioritisation. |
| Mixed | Mixed | Mixed | Low | Mixed | Several findings already adequately represented by higher-priority behavioural themes. | Avoid unnecessary repetition of behaviourally redundant information. |
| Mixed | Mixed | Mixed | Low | Mixed | Duplicate findings describing essentially the same behavioural change. | Redundant information should not occupy assessment space unnecessarily. |

---

# Applying the Priority Reference Table

The Constitution always takes precedence over this Priority Reference Table.

This table demonstrates representative prioritisation decisions rather than replacing behavioural reasoning.

The V2 Attention Filter should never determine behavioural importance using a single characteristic in isolation.

Instead, priority should emerge from the combined interpretation of:

- Current Effect
- Severity
- Behavioural State
- Journal Evidence
- Related Supporting Findings
- Overall Behavioural Context

The examples within this table intentionally illustrate situations where these factors interact.

For example:

- A **High Severity Harmful Resolving** finding may remain within **Tier 1** if the current harmful behavioural effect remains substantial.

- The same finding may reasonably receive **Tier 3** attention if journal evidence consistently demonstrates meaningful recovery while another finding indicates rapidly worsening behaviour.

Similarly,

- A **High Severity Beneficial Persistent** finding may deserve greater attention than several unrelated low-severity harmful findings because it represents a consistently demonstrated behavioural strength with substantial behavioural significance.

The objective of the V2 Attention Filter is **not rigid consistency**.

The objective is **behaviourally meaningful prioritisation**.

---

# Relationship with the Assessment Trigger Policy

This Priority Reference Table also serves as the prioritisation reference used by the Assessment Trigger Policy.

The Assessment Trigger Policy determines:

- Whether a V2 Assessment should be generated.
- Whether the assessment is automatically triggered or user-requested.
- How many prioritised findings should be forwarded to the V2 Assessment Prompt.

The V2 Attention Filter determines:

- Which findings deserve attention.
- Their relative behavioural importance.
- Their Priority Tier.

Consequently, the Assessment Trigger Policy should rely upon the prioritised output produced by the V2 Attention Filter rather than independently reprioritising findings.

For automatically triggered assessments, the Trigger Policy may forward only the highest-priority findings.

For user-requested assessments, the Trigger Policy may forward a larger number of prioritised findings to provide a more comprehensive behavioural assessment.

However, the relative ordering of findings should always remain consistent with the prioritisation established by the V2 Attention Filter.

---

# Final Notes

The responsibility of the V2 Attention Filter ends once behavioural findings have been appropriately prioritised.

Its output should consist solely of prioritised findings together with the attributes that justify their selection.

The V2 Attention Filter must **never**:

- synthesise behavioural themes,
- merge related findings into broader psychological concepts,
- construct narrative explanations,
- infer psychological causes,
- generate recommendations,
- determine assessment wording,
- or produce the final behavioural assessment.

Those responsibilities belong exclusively to the **V2 Assessment Prompt**.

Maintaining this separation preserves the Single Responsibility Principle within the Mental Health Assessment framework.

The V2 Attention Filter determines **what deserves attention**.

The V2 Assessment Prompt determines **how those findings should be interpreted, synthesised and communicated**.

This separation improves behavioural consistency, modularity, explainability and long-term maintainability of the assessment framework.