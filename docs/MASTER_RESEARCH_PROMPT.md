# Master Research Execution Prompt

Use this prompt with ChatGPT, Codex, Claude Code, GitHub Copilot, or another capable coding/research agent that has access to this repository and the authorized datasets.

---

## MASTER PROMPT

You are the lead research engineer, statistician, and publication-quality scientific editor for the project:

**Beyond Static Accuracy: Drift-Aware, Calibration-Safe, Explanation-Stable, and Cost-Sensitive Customer Behavior Prediction in Banking and Insurance**

Repository: `Arungharami/Customer-Behavior-Prediction-in-Banking-and-Insurance-2`

### Mission

Build and execute a fully reproducible empirical pipeline that produces a journal-ready Part 2 study using public real-world/industry benchmark data. The study must advance beyond static accuracy by jointly evaluating temporal stability, probability calibration, explanation stability, decision cost, uncertainty, and computational complexity.

### Non-negotiable research-integrity rule

**Never fabricate or estimate experimental results.** Every numerical result in the manuscript must come from an executed artifact. If a result has not been executed, write `NOT EXECUTED` and stop that claim from entering Results, Discussion, Abstract, or Conclusion.

Do not invent references, DOIs, dataset provenance, sample sizes, model scores, p-values, confidence intervals, latency, memory, model size, or economic benefits.

### Primary datasets

1. Home Credit - Credit Risk Model Stability (Kaggle) - primary temporal/stability benchmark.
2. UCI Bank Marketing - banking product-uptake benchmark, using the date-ordered full dataset where available.
3. Porto Seguro Safe Driver Prediction - insurance claim-propensity external-validation benchmark.
4. IEEE-CIS Fraud Detection - optional supplementary fraud benchmark only if compute and manuscript length allow.

Do not redistribute Kaggle raw files in GitHub. Record competition/data URLs, dataset versions, checksums, download date, and applicable rules/licenses in manifests.

### Research questions

RQ1. How much do discrimination and calibration deteriorate under later-time evaluation compared with random or in-time validation?

RQ2. Which models provide the best accuracy-stability-calibration trade-off across banking and insurance datasets?

RQ3. Are SHAP explanations stable across time windows and population shifts, or can the apparent decision logic change while aggregate accuracy remains acceptable?

RQ4. Does a complex ensemble provide enough incremental value to justify its training cost, inference latency, memory footprint, and model size relative to a simpler gradient-boosting model?

RQ5. Do cost-sensitive and capacity-constrained thresholds provide more reliable operational value than fixed probability thresholds?

### Required baselines

Train Logistic Regression, Random Forest, XGBoost, LightGBM, and CatBoost. Add a stability-aware ensemble only after all standalone baselines are frozen. Optionally evaluate a modern tabular foundation model on a clearly documented resource-feasible subset; label it exploratory and do not let it replace strong tree baselines.

### Leakage controls

- Identify entity keys and time variables before modeling.
- Do not allow future observations into feature windows.
- Perform preprocessing, target encoding, imputation, feature selection, and calibration inside training folds/windows only.
- For Home Credit, use time-aware folds based on the competition time index/week variable.
- For Bank Marketing, preserve the original chronological ordering; never use `duration` for pre-contact deployment claims because it is only known after the call.
- Never use target-derived features.
- Write automated leakage tests and fail the pipeline if they fail.

### Evaluation protocol

For each dataset/model/window produce:

- ROC-AUC
- PR-AUC / Average Precision
- precision, recall, F1
- Brier score
- ECE
- calibration slope and intercept
- bootstrap 95% confidence intervals
- fixed-capacity metrics: Precision@k%, Recall@k%, Lift@k%
- train wall time
- inference p50 and p95 latency
- peak memory
- serialized model size

For temporal datasets additionally produce:

- metric by time window
- slope of performance over time
- PSI for monitored features
- univariate KS/Wasserstein or Jensen-Shannon drift statistics as appropriate
- model-score drift
- calibration drift
- Home Credit competition stability score where applicable

### Calibration

Compare raw probabilities against Platt/sigmoid and isotonic calibration using calibration data that are chronologically later than training but earlier than final test. Never calibrate on the final holdout.

### Explainability stability

Use SHAP on the frozen best tree/ensemble models. Produce:

- global beeswarm for an early window
- global beeswarm for a late window
- top-20 feature table for each window
- Spearman correlation of global mean-|SHAP| ranks
- Jaccard overlap for top-10/top-20 features
- selected local waterfall explanations for correctly predicted and error cases

When comparing explanations across windows, use identical feature definitions and a documented sampling procedure.

### Cost-sensitive decision analysis

Use transparent scenario parameters rather than claiming proprietary bank economics. Report results across a sensitivity grid instead of a single invented cost assumption. For each task define TP benefit, FP cost, FN cost, and intervention capacity. Produce net-benefit curves across thresholds/capacities and identify regions where the preferred model changes.

### Fairness and governance

Only compute group fairness where the dataset legitimately contains relevant attributes and their use is permitted. Report subgroup AUC/calibration and equal-opportunity-style gaps as an audit, not as proof of legal compliance. Explicitly discuss proxy risk and limitations.

### Statistical rigor

- Freeze all test windows before model tuning.
- Use repeated or nested time-aware validation where feasible.
- Use paired bootstrap comparisons for model deltas.
- Report effect sizes and CIs, not only p-values.
- Correct for multiple comparisons when many hypotheses are tested.
- Set and record all random seeds.

### Required ablations

At minimum run:

A1. Remove temporal features.
A2. Remove relational/high-cardinality features where present.
A3. Uncalibrated vs calibrated probabilities.
A4. Single best booster vs stacked/stability-aware ensemble.
A5. Random split vs time-aware split on temporal datasets.
A6. Accuracy-only model selection vs stability-aware selection.

### Required figures - fixed numbering

Figure 1. Research framework and end-to-end trustworthy prediction pipeline.
Figure 2. Dataset timeline and leakage-safe temporal evaluation design.
Figure 3. Dataset/task characteristics and class imbalance.
Figure 4. Model discrimination across datasets/tasks.
Figure 5. Performance stability across time windows.
Figure 6. Calibration reliability diagrams before and after recalibration.
Figure 7. Feature/data drift dashboard.
Figure 8. SHAP explanation stability: early vs late window.
Figure 9. Accuracy-calibration-stability-efficiency Pareto frontier.
Figure 10. Cost/capacity net-benefit analysis.

Do not renumber these casually. If a figure is removed, update the registry, manuscript, captions, and all cross-references in one atomic change.

### Required tables - fixed numbering

Table 1. Dataset provenance, task, size, period/time index, target, imbalance, and usage constraints.
Table 2. Feature families and leakage controls.
Table 3. Model families and tuned hyperparameters.
Table 4. Main held-out performance with 95% CIs.
Table 5. Temporal stability and calibration metrics.
Table 6. Explanation-stability metrics.
Table 7. Computational cost and model complexity.
Table 8. Cost-sensitive/capacity-constrained operational outcomes.
Table 9. Ablation study.

### Artifact contract

All generated outputs must be stored under a deterministic run directory such as:

`artifacts/runs/<run_id>/`

with:

- `config_snapshot.yaml`
- `environment.txt`
- `git_commit.txt`
- `data_manifest.json`
- `metrics/*.csv`
- `figures/figure_01_*.png` ... `figure_10_*.png`
- `tables/table_01_*.csv` ... `table_09_*.csv`
- `models/`
- `logs/`

Create `artifacts/latest.json` pointing to the accepted run.

### Publication writing rules

Write the paper only from the accepted artifact set. Keep the manuscript within the journal's current word limit. Use natural academic prose, not templated filler. Avoid overstating causality, generalizability, regulatory compliance, or business benefit.

Every Results claim must cite a table or figure. Every number in Abstract and Conclusion must be traceable to the same accepted artifact run.

Use APA 7th edition references and verify each bibliographic record against the primary publisher, paper, or official organization source.

### Final gates

GATE 1 - Data provenance and rules documented.
GATE 2 - Leakage tests pass.
GATE 3 - Baselines executed.
GATE 4 - Temporal/drift and calibration analyses executed.
GATE 5 - SHAP stability executed.
GATE 6 - complexity/latency and cost analysis executed.
GATE 7 - ablations and uncertainty intervals executed.
GATE 8 - every figure/table generated and registry validated.
GATE 9 - manuscript numbers match artifacts exactly.
GATE 10 - blind-manuscript formatting, APA references, figure numbering, captions, alignment, and metadata pass final QA.

If any gate fails, stop and report the failure. Do not fill missing results with plausible values.

### Deliverables

1. Reproducible source code and environment.
2. Executed artifact package.
3. Small best-performing practical model bundle and model card for Hugging Face.
4. Clean blind manuscript.
5. Separate title page.
6. Response-to-reviewers/cover letter if required.
7. Supplementary reproducibility appendix.
8. README with one-command reproduction instructions.

---

End of master prompt.
