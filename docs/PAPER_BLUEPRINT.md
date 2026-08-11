# Part 2 Publication Blueprint

## Recommended final title

**Beyond Static Accuracy: Temporal Stability, Probability Calibration, Explanation Stability, and Cost-Sensitive Customer Behavior Prediction in Banking and Insurance**

## Positioning relative to Part 1

Part 1 established a unified applied prediction pipeline. Part 2 must make a distinct contribution by testing whether financial models remain trustworthy after deployment conditions change. The manuscript should emphasize **temporal stability, calibration, explanation stability, operational utility, and model complexity**, not repeat the original static comparison.

## Central novelty statement

Most applied financial prediction papers report discrimination on a fixed test set. This study evaluates whether models remain useful when data distributions shift by jointly measuring discrimination, temporal degradation, calibration, explanation stability, decision cost, and computational complexity across banking and insurance benchmarks.

## Recommended empirical design

### Primary benchmark: Home Credit - Credit Risk Model Stability
Use as the central temporal/stability experiment. Preserve the competition time index. Compare accuracy-only selection with stability-aware selection.

### Banking external validation: UCI Bank Marketing
Use the full date-ordered data. Evaluate term-deposit uptake. Exclude the call-duration feature from realistic pre-contact prediction because it is not known before the marketing call finishes.

### Insurance external validation: Porto Seguro Safe Driver
Use claim propensity as the insurance case study. Report Gini in addition to the project's common metrics when useful for compatibility with the original competition.

### Optional fraud supplement: IEEE-CIS
Only include if compute, manuscript length, and artifact quality remain manageable. Do not weaken the main story merely to add a fourth dataset.

## Model strategy

### Tier 1 - interpretable baseline
Logistic Regression.

### Tier 2 - conventional nonlinear baselines
Random Forest, XGBoost, LightGBM, CatBoost.

### Tier 3 - proposed deployment model
A stability-aware calibrated ensemble selected using a multi-objective score combining predictive discrimination, calibration loss, and temporal degradation. The formula and weights must be pre-specified and sensitivity-tested.

### Tier 4 - modern exploratory benchmark
TabPFN or another tabular foundation model may be tested only on an explicitly resource-feasible subsample because the primary datasets are much larger than the small/medium regime where such models are most appropriate. It should be presented as an exploratory comparison, not the paper's main contribution.

## Methods sections

### 3.1 Datasets and provenance
Give source, task, size, time coverage/index, target prevalence, and data-use restrictions. Avoid describing competition datasets as proprietary data collected by the author.

### 3.2 Leakage-safe temporal design
Freeze train, calibration, and final test windows. Include Figure 2.

### 3.3 Feature processing
Document categorical handling, missing data, feature exclusion, and the rule that all preprocessing is fit on training data only.

### 3.4 Predictive models
Describe each baseline and the proposed stability-aware model without unnecessary textbook exposition.

### 3.5 Calibration
Evaluate raw, sigmoid/Platt, and isotonic probability calibration using a chronologically separate calibration window.

### 3.6 Drift monitoring
Measure PSI, feature-distance metrics, score drift, and time-window performance. Distinguish covariate shift from observed performance drift; do not claim concept drift solely from feature distribution changes.

### 3.7 Explanation stability
Compute SHAP on frozen models across early and late windows; compare feature ranks and top-k overlap.

### 3.8 Operational evaluation
Use capacity-based metrics and a sensitivity grid of TP benefit, FP cost, and FN cost. Avoid presenting one assumed dollar value as if it were a verified bank accounting figure.

### 3.9 Complexity
Record training time, model size, RAM, and inference p50/p95. This section directly answers whether stacking is operationally justified.

### 3.10 Statistics
Use bootstrap confidence intervals and paired resampling for model deltas. Report effect sizes and uncertainty.

## Results order

1. Dataset characteristics - Table 1 / Figure 3.
2. Main held-out performance - Table 4 / Figure 4.
3. Temporal stability - Table 5 / Figure 5.
4. Calibration - Table 5 / Figure 6.
5. Drift - Figure 7.
6. Explanation stability - Table 6 / Figure 8.
7. Accuracy/stability/efficiency trade-off - Table 7 / Figure 9.
8. Operational sensitivity - Table 8 / Figure 10.
9. Ablation study - Table 9.

## Discussion structure

### What improved over Part 1
Explain why temporal and external validation change the interpretation of model quality.

### When complexity is justified
Explicitly compare the incremental predictive gain against latency/model-size/calibration/stability costs.

### Explainability under change
Discuss whether feature importance remains stable and why a static SHAP screenshot is insufficient for long-lived financial models.

### Operational implications
Discuss ranking under fixed capacity and cost sensitivity without claiming realized profit.

### Governance implications
Describe monitoring, recalibration, human oversight, documentation, and periodic review. Do not claim that SHAP alone establishes regulatory compliance.

### Limitations
Public competition datasets are anonymized and differ in task definitions; temporal coverage is uneven; cost values are scenarios; external validation does not prove universal generalization; fairness audits may be limited by available protected-attribute data.

## Abstract formula

The final abstract should contain only executed values:

- problem/gap: 1-2 sentences;
- datasets and temporal protocol: 1 sentence;
- models + calibration/drift/XAI: 1 sentence;
- 2-4 most important executed findings with CIs where space allows;
- operational/complexity implication: 1 sentence;
- conclusion limited to what the results directly support.

## Strong contribution claims that are acceptable if supported by executed results

- jointly evaluates predictive discrimination, calibration, explanation stability, operational value, and computational complexity under temporal shift;
- provides a reproducible multi-dataset banking/insurance benchmark;
- shows when the model with the best static AUC is not the best deployment choice;
- quantifies explanation instability rather than showing only static SHAP plots;
- evaluates the value of calibration and stability-aware model selection through ablations.

## Claims to avoid

- "first ever" without a systematic review proving it;
- "regulatory compliant";
- "real-world profit increased by X%" when using simulated costs;
- "concept drift detected" based only on PSI;
- "causal drivers" from SHAP associations;
- "industry-ready" without external institutional validation.
