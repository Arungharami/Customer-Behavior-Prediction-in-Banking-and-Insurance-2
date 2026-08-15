# Stage 1 — Research Question and Contribution Freeze

**Freeze date:** 2026-08-15  
**Status:** `FROZEN_PENDING_DATASET_VALIDATION`

## Working title

**Beyond Static Accuracy: Drift-Aware, Explanation-Stable, and Cost-Sensitive Customer Behavior Prediction in Banking and Insurance**

The final title may be shortened for journal style, but the scientific scope must not expand after final test windows are observed.

## Central research question

> Can banking and insurance customer-behavior prediction systems remain discriminative, calibrated, explanation-stable, and decision-useful under realistic temporal distribution shift?

## Frozen research questions

### RQ1 — Temporal generalization
How much does predictive performance change when models are evaluated prospectively with chronological/rolling-origin evaluation rather than conventional static or random evaluation, when a valid comparison is possible?

### RQ2 — Drift
How do feature distributions, outcome prevalence, and model-score distributions change across chronological periods, and which shifts coincide with material performance degradation?

### RQ3 — Calibration
Do models that retain acceptable ranking performance remain probabilistically reliable under temporal shift, and can leakage-safe post-hoc recalibration improve later-window probability quality?

### RQ4 — Explanation stability
Are global feature-attribution rankings stable across chronological periods and model families, and can explanation instability occur without corresponding discrimination loss (or vice versa)?

### RQ5 — Decision utility
Do model rankings change when asymmetric false-positive/false-negative costs and fixed intervention capacities are considered rather than ranking models only by ROC-AUC?

### RQ6 — Complexity versus robustness
Does the most complex reproducible model provide enough improvement in temporal robustness, calibration, explanation stability, or scenario-dependent decision utility to justify additional training, inference, model-size, and monitoring burden?

## Non-directional hypotheses

No hypothesis is framed to require an advanced model to win. The analysis must preserve and report negative or null findings.

- **H1:** Temporal evaluation may produce materially different model rankings or uncertainty than random/static evaluation.
- **H2:** Distribution shift may occur without a proportional decline in discrimination.
- **H3:** Calibration may degrade independently of ROC-AUC/PR-AUC.
- **H4:** Explanation rankings may change across time even when predictive performance appears stable.
- **H5:** The model with the highest discrimination may not minimize scenario-dependent decision cost or maximize utility under capacity constraints.
- **H6:** A simpler model may be preferred when incremental predictive benefit from a complex ensemble is small relative to complexity costs.

These are testable expectations, not assumed results.

## Core contribution claim — allowed before execution

The methodological contribution is the **evaluation framework**, not any unexecuted performance claim:

> Part 2 evaluates financial customer-behavior models jointly across prospective temporal generalization, probability calibration, distribution drift, explanation stability, decision utility, computational complexity, and reproducibility, with explicit prediction-time leakage controls and artifact-level claim traceability.

## Claims prohibited until executed evidence exists

Do not write any of the following unless the accepted artifact set directly supports them:

- one model is “best,” “superior,” “robust,” or “stable”;
- AUC/PR-AUC/Brier/ECE values or improvements;
- statistically significant model differences;
- fraud/churn/cross-sell savings or percentage improvements;
- SHAP feature rankings or stability values;
- drift magnitude or drift-trigger effectiveness;
- fairness performance;
- latency, memory, throughput, or model-size values;
- regulatory compliance;
- real-world deployment benefit.

Use `NOT_EXECUTED`, `NOT_MEASURED`, `INSUFFICIENT_EVIDENCE`, or `REQUIRES_VALIDATION` until the relevant gate passes.

## Dataset strategy freeze

### Primary temporal benchmark
**Home Credit — Credit Risk Model Stability**, contingent on authorized competition access and rule/license documentation.

### Banking external validation
**UCI Bank Marketing**, using the original-source release where possible. `duration` must be excluded from any pre-contact deployment-style prediction because it is known only after the marketing call.

### Insurance external validation
**Porto Seguro Safe Driver Prediction**, contingent on authorized competition access and rule/license documentation.

### Optional fraud stress test
**IEEE-CIS Fraud Detection**, disabled by default and included only if compute, licensing, artifact quality, and manuscript-length constraints permit.

### Part 1 institutional dataset
The Part 1 120,000-customer dataset is **not assumed available**. It may be used only if source data, authorization, timestamps, labels, and prediction-time feature provenance are independently revalidated for Part 2. Otherwise Part 2 will be explicitly reframed as a reproducible public-benchmark extension rather than a re-analysis of the proprietary/institutional environment.

## Prediction horizon rule

A common 90-day horizon is preferred **only where the source data permit exact reconstruction**. It must not be fabricated from datasets that provide a task-native target without reconstructible event timestamps. For such datasets, use and clearly report the task-native horizon/label definition or exclude the task from horizon-specific analyses.

## Model benchmark freeze

Minimum required benchmark:

1. Logistic Regression
2. Random Forest
3. XGBoost
4. Part 1-compatible stack, **if faithfully reproducible**

Additional prespecified baselines:

5. LightGBM
6. CatBoost

Optional exploratory model classes must be labeled exploratory and may not replace the required baselines.

### Ensemble definition rule

The existing repository stack (`XGBoost + LightGBM + CatBoost → Logistic Regression`) is not the same as the Part 1 stack described in the prior manuscript (`Random Forest + XGBoost → Logistic Regression`). Before execution, the implementation must either:

- add a faithful `part1_stack` configuration, or
- rename the current model as a new `part2_stability_ensemble` and treat it as a separate advanced baseline.

Do not conflate them in the manuscript.

## Temporal protocol freeze

The central protocol is rolling-origin/forward-chaining evaluation. Conceptually:

- Train T1 → Test T2
- Train T1–T2 → Test T3
- Train T1–T3 → Test T4
- continue while sufficient observations/classes remain

Within each origin, all fit operations must use only information available before the evaluated period:

- imputation
- scaling
- categorical encoding
- feature selection
- target encoding
- hyperparameter selection
- calibration
- threshold selection

Future test windows are never used to choose models or thresholds.

## Metrics freeze

Where mathematically defined and appropriate:

### Discrimination
- ROC-AUC
- PR-AUC / Average Precision
- precision
- recall / sensitivity
- specificity
- F1
- confusion matrix

### Probability quality
- Brier score
- log loss
- ECE (with binning documented)
- calibration slope
- calibration intercept
- reliability curves

### Operational ranking
- Precision@capacity
- Recall@capacity
- Lift@capacity

### Complexity
- training wall time
- p50 inference latency
- p95 inference latency
- throughput
- serialized model size
- peak memory where reliably measurable

## Drift freeze

Use metrics by variable type and state their assumptions. Candidate measures:

- PSI for monitored numeric/categorical distributions with fixed reference bins/categories;
- Wasserstein distance for numeric variables;
- KS statistic for continuous numeric distributions where appropriate;
- Jensen–Shannon divergence for comparable discrete/probability distributions;
- event/prevalence drift;
- prediction-score drift;
- performance drift;
- calibration drift.

Do not call feature-distribution change “concept drift” without evidence of changed predictor–outcome relationships.

## Explanation-stability freeze

For executable tree-based models, save per-window SHAP source artifacts and compare:

- global mean absolute SHAP values;
- Spearman rank correlation;
- top-k Jaccard overlap (k = 10, 20 when enough features exist);
- rank displacement;
- direction/sign consistency where the attribution definition supports it;
- selected local explanations with prespecified sampling logic.

Permutation importance may be used as a cross-method diagnostic; disagreement is a result to report, not a reason to suppress a method.

## Cost-sensitive analysis freeze

Cost analysis is scenario-based unless genuine organization-approved economics are available. Use prespecified grids and report normalized utility/cost. Thresholds must be selected on training/calibration information and frozen before each future test period.

No scenario result may be worded as realized bank/insurance profit or verified savings.

## Statistical policy freeze

- Report fold/window-level values.
- Use paired comparisons when models share exactly the same evaluation observations/folds.
- Prefer grouped or clustered resampling when repeated observations from the same entity exist.
- Report effect sizes and uncertainty, not only p-values.
- Apply multiplicity correction only where a family of confirmatory tests is actually conducted.
- Do not perform formal significance tests when fold count or dependence makes inference misleading; report descriptive uncertainty and state the limitation.

## Canonical publication artifact registry decision

The latest master protocol proposes **Figures 1–9** and **Tables 1–11**. The current code gate expects Figures 1–10 and Tables 1–9. To avoid late numbering errors, the project will adopt the following final registry unless the journal format forces consolidation **before** empirical results are frozen:

### Figures
1. Research and deployment-oriented analytical pipeline
2. Dataset timeline and rolling-origin evaluation design
3. Temporal model-performance trajectories
4. Feature/prediction drift analysis
5. Calibration/reliability across time
6. SHAP explanation-stability analysis
7. Performance versus explanation-stability relationship
8. Cost-sensitive threshold/decision-utility analysis
9. Accuracy–calibration–stability–complexity trade-off

### Tables
1. Dataset and task characteristics
2. Prediction-time feature taxonomy
3. Temporal evaluation protocol
4. Model configurations
5. Fold-level predictive performance
6. Calibration results
7. Drift measurements
8. Explanation-stability results
9. Cost-sensitive decision analysis
10. Robustness/ablation findings
11. Comparison with prior literature

The publication gate must be updated to this registry before any accepted empirical run is declared publication-ready.

## Stage 1 decision

**Stage 1: PASS.**

The research questions, non-fabrication constraints, dataset strategy, model benchmark, temporal protocol, metric families, and publication artifact numbering are now frozen subject only to evidence-driven exclusions (e.g., a dataset lacking usable time semantics). The next stage is **Stage 2 — dataset provenance and licensing**.
