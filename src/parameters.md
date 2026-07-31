# Mental Health Parameters

## Purpose

This document defines the **Mental Health Parameters** measured by the Mental Health Digital Twin. It serves as the authoritative specification for every parameter used throughout the project.

The term **Mental Health Parameters** refers to the complete set of parameters measured by the system.

The term **Behavioural Parameters** refers **only** to the Behavioural domain (Task Engagement, Motivation, Coping Ability, Resilience and Emotional Exhaustion). It must never be used as a collective name for the complete parameter set.

> **Note**
>
> The Mental Health Parameters are operational constructs designed specifically for this Mental Health Digital Twin. They represent behavioural characteristics inferred from journal entries and are intended for behavioural assessment and longitudinal monitoring. They are **not** clinical diagnoses or validated psychological scales.

Behaviour-related phrases such as **behavioural assessment**, **behavioural interpretation**, **behavioural progression**, **behavioural patterns**, and **behavioural state** retain their normal meaning throughout the repository.

---

# Parameter Taxonomy

Every Mental Health Parameter belongs to **two independent classifications**:

1. Classification by Calculation Method
2. Classification by Domain

---

# 1. Classification by Calculation Method

## Immediate Parameters

Immediate Parameters represent the user's current mental state as expressed within an individual journal entry.

Characteristics:

- Calculated from every journal entry beginning with Entry 1.
- Personalised baseline maintained using an **Exponentially Weighted Moving Average (EWMA)**.
- Fully processed by the anomaly detection framework.

Immediate Parameters possess:

- Baseline
- Anomaly Score
- Anomaly Severity
- Anomaly Direction
- Anomaly Polarity
- Persistence
- Historical anomaly information

### Immediate Parameters

- Sentiment Score
- Stress
- Anxiety
- Sadness
- Frustration
- Optimism
- Concentration
- Self-talk Score
- Task Engagement
- Motivation
- Coping Ability
- Social Connectedness
- Social Support
- Self-efficacy
- Sleep Quality

---

## Long-Term Parameters

Long-Term Parameters represent behavioural capacities that evolve gradually rather than changing substantially after a single journal entry.

These parameters are computed using sliding windows.

| Parameter | Window |
|-----------|--------|
| Rumination | 7 Entries |
| Mental Fatigue | 10 Entries |
| Physical Fatigue | 10 Entries |
| Emotional Exhaustion | 14 Entries |
| Resilience | Context-dependent |

Since each computed value already represents behaviour across multiple journal entries:

- Current Value = Current Baseline
- No additional EWMA baseline is computed.
- These parameters bypass the anomaly detection framework.

Long-Term Parameters therefore do **not** possess:

- Anomaly Score
- Anomaly Severity
- Anomaly Direction
- Anomaly Polarity
- Persistence

---

# 2. Classification by Domain

## Emotional Parameters

- Sentiment Score
- Stress
- Anxiety
- Sadness
- Frustration
- Optimism

---

## Psychological Parameters

- Concentration
- Mental Fatigue
- Rumination
- Self-talk Score

---

## Behavioural Parameters

- Task Engagement
- Motivation
- Coping Ability
- Resilience
- Emotional Exhaustion

---

## Social Parameters

- Social Connectedness
- Social Support
- Self-efficacy

---

## Physical Parameters

- Sleep Quality
- Physical Fatigue

---

# Operational Definitions

| Parameter | Operational Definition |
|-----------|------------------------|
| **Sentiment Score** | The overall emotional tone expressed within the journal entry, representing how positive or negative the user's experience appears. |
| **Stress** | The degree to which the user expresses feeling pressured, overwhelmed or mentally burdened by current demands. |
| **Anxiety** | The extent to which the user expresses worry, uncertainty or anticipation regarding future events or outcomes. |
| **Sadness** | The degree of low mood, disappointment or emotional distress expressed within the journal. |
| **Frustration** | The extent to which the user expresses irritation arising from obstacles, setbacks or unmet expectations. |
| **Optimism** | The degree of hopefulness and positive expectation regarding future situations or personal outcomes. |
| **Concentration** | The user's ability to maintain attention, remain mentally focused and effectively process information while performing tasks. |
| **Mental Fatigue** | The accumulated decline in cognitive energy and mental efficiency resulting from sustained psychological effort over time. |
| **Rumination** | The long-term tendency to repeatedly dwell on negative thoughts, mistakes or unresolved concerns. |
| **Self-talk Score** | The overall quality of the user's internal dialogue, ranging from self-supportive to self-critical thinking. |
| **Task Engagement** | The extent to which the user actively participates in and follows through with planned academic or daily activities. |
| **Motivation** | The user's willingness and drive to initiate and persist with goal-directed activities. |
| **Coping Ability** | The user's current capacity to adapt to challenges, manage stressors and continue functioning despite difficulties. |
| **Resilience** | The long-term capacity to recover from setbacks and progressively regain effective functioning following adversity. |
| **Emotional Exhaustion** | The accumulated depletion of emotional energy caused by prolonged psychological demands or stress. |
| **Social Connectedness** | The degree to which the user feels connected to, engaged with and emotionally involved in social interactions. |
| **Social Support** | The extent to which the user perceives emotional or practical support to be available from others. |
| **Self-efficacy** | The user's confidence in their ability to successfully handle challenges and achieve intended goals. |
| **Sleep Quality** | The perceived quality, restfulness and consistency of the user's sleep. |
| **Physical Fatigue** | The accumulated level of bodily tiredness and reduced physical energy developing over time. |

---

# Combined Reference

| Parameter | Calculation Method | Domain |
|-----------|--------------------|--------|
| Sentiment Score | Immediate | Emotional |
| Stress | Immediate | Emotional |
| Anxiety | Immediate | Emotional |
| Sadness | Immediate | Emotional |
| Frustration | Immediate | Emotional |
| Optimism | Immediate | Emotional |
| Concentration | Immediate | Psychological |
| Mental Fatigue | Long-Term | Psychological |
| Rumination | Long-Term | Psychological |
| Self-talk Score | Immediate | Psychological |
| Task Engagement | Immediate | Behavioural |
| Motivation | Immediate | Behavioural |
| Coping Ability | Immediate | Behavioural |
| Resilience | Long-Term | Behavioural |
| Emotional Exhaustion | Long-Term | Behavioural |
| Social Connectedness | Immediate | Social |
| Social Support | Immediate | Social |
| Self-efficacy | Immediate | Social |
| Sleep Quality | Immediate | Physical |
| Physical Fatigue | Long-Term | Physical |

---

# Repository Usage

This document acts as the central specification for every Mental Health Parameter used throughout the project.

- The **Data Module** computes parameter values.
- The **Anomaly Module** analyses only Immediate Parameters.
- **Stage 1** interprets both Immediate and Long-Term Parameters.
- **Stage 2** performs longitudinal behavioural reasoning using both parameter categories.
- **Stage 3** assesses potential psychological conditions using the behavioural assessment produced by the previous stages.

Any modification to parameter definitions, classifications or calculation methods should be made in this document before being propagated throughout the remainder of the project.