# V1 Attention Filter

---

# Objective

The V1 Attention Filter is a temporary filtering mechanism used after the user's initial personal baseline has been established but before the anomaly detection module becomes active.

Its sole responsibility is to determine which behavioural parameters deserve attention by comparing their current baseline values against a predefined reference range.

The V1 Attention Filter does **not** prioritise findings, analyse journal entries, infer behavioural causes or generate assessments. Its output serves only as the input to the V1 Trigger Policy and V1 Assessment Prompt.

---

# Operating Period

The V1 Attention Filter becomes active only after the initial personal baseline has been established.

It operates during the transitional period between:

- completion of Entry 20, and
- activation of the anomaly detection module.

Once the anomaly detection module becomes available, the V1 Attention Filter must become dormant.

---

# V1 Reference Range

During the V1 period, every parameter baseline is evaluated using the following reference range:

```text
3.5 ≤ Baseline ≤ 6.5
```

Any baseline value within this range is considered to lie within the expected operating range.

Baseline values outside this range require further classification.

---

# Parameter Polarity

Every behavioural parameter must already be classified as either:

- **Positive Parameter**
- **Negative Parameter**

This polarity determines whether a deviation outside the reference range is behaviourally beneficial or behaviourally concerning.

---

## Positive Parameters

For positive parameters:

| Baseline | Classification |
|-----------|----------------|
| Baseline > 6.5 | Beneficially Outside the Range |
| 3.5 ≤ Baseline ≤ 6.5 | Within the Range |
| Baseline < 3.5 | Concerningly Outside the Range |

---

## Negative Parameters

For negative parameters:

| Baseline | Classification |
|-----------|----------------|
| Baseline < 3.5 | Beneficially Outside the Range |
| 3.5 ≤ Baseline ≤ 6.5 | Within the Range |
| Baseline > 6.5 | Concerningly Outside the Range |

---

# Filtering Process

For every behavioural parameter:

1. Identify the parameter polarity.

2. Compare the current baseline against the V1 reference range.

3. Classify the parameter as one of:

   - Within the Range
   - Beneficially Outside the Range
   - Concerningly Outside the Range

4. If the parameter lies outside the reference range, determine how far the baseline lies beyond the nearest boundary.

This distance represents the magnitude of deviation from the expected V1 range and should be forwarded together with the finding.

No behavioural interpretation should occur during this stage.

---

# Measuring Deviation

For parameters classified as being outside the reference range, calculate the deviation as the absolute distance from the nearest range boundary.

For example:

```text
Negative Parameter

Baseline = 7.9

Deviation = 7.9 − 6.5 = 1.4
```

```text
Positive Parameter

Baseline = 2.8

Deviation = 3.5 − 2.8 = 0.7
```

A larger deviation indicates that the baseline lies further outside the expected V1 range.

The V1 Attention Filter should not interpret whether one deviation deserves greater attention than another. It simply measures and forwards the deviation.

---

# Output

For every parameter classified as being outside the reference range, the V1 Attention Filter should produce:

- Parameter
- Parameter Polarity
- Current Baseline
- Classification
- Direction of Deviation
- Distance Beyond the Reference Range

For example:

```text
Parameter:
Stress

Polarity:
Negative

Baseline:
7.8

Classification:
Concerningly Outside the Range

Direction:
Above Upper Boundary

Deviation:
1.3
```

or

```text
Parameter:
Optimism

Polarity:
Positive

Baseline:
2.9

Classification:
Concerningly Outside the Range

Direction:
Below Lower Boundary

Deviation:
0.6
```

Parameters lying beneficially outside the reference range may also be forwarded when required for balanced assessment.

---

# Boundaries

The V1 Attention Filter must not:

- analyse journal entries,
- identify behavioural causes,
- generate recommendations,
- prioritise findings,
- compare recent behavioural trends,
- generate behavioural themes,
- construct narrative assessments,
- or determine whether an assessment should be produced.

Those responsibilities belong to the subsequent V1 Trigger Policy and V1 Assessment Prompt.

---

# Role Within the V1 Pipeline

The V1 Attention Filter answers a single question:

> **Which behavioural parameters currently lie inside or outside the V1 reference range, and by how much?**

It provides only the information required for the next stages of the V1 assessment process.

Its output should therefore remain objective, descriptive and free from behavioural interpretation.