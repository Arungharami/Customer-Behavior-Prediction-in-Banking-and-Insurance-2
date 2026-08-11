# Small Hugging Face Deployment Model Plan

## Goal

Publish a **compact practical model**, not the heaviest research ensemble, so the repository demonstrates both scientific accuracy and deployment discipline.

## Recommended strategy

1. Train all required research baselines.
2. Select the strongest stable/calibrated teacher model or ensemble on the frozen validation protocol.
3. Train a compact CatBoost or LightGBM student model using the original labels and, optionally, teacher soft probabilities as an auxiliary distillation target.
4. Calibrate the student using the dedicated calibration window.
5. Compare student vs teacher on:
   - ROC-AUC and PR-AUC
   - Brier score and ECE
   - temporal stability slope
   - SHAP rank stability
   - p50/p95 latency
   - serialized size
   - peak memory
6. Publish the student only if its practical trade-off is defensible. Do not declare success until executed results support it.

## Suggested Hugging Face repository

`arun-gharami/customer-behavior-prediction-banking-insurance-part2`

## Required files

- serialized model (`model.cbm`, `model.txt`, or `model.joblib`)
- preprocessing contract/schema
- `metadata.json`
- `README.md` model card
- example inference script
- accepted run ID and Git commit

## Model card warnings

The model card must state that the artifact is for research/educational use and is not independently validated for production lending, underwriting, pricing, fraud adjudication, or other high-stakes automated decisions.

## Why this strengthens the paper

This small-model track directly answers the reviewer concern that a marginal predictive gain may not justify a stacked ensemble. The paper can report a **teacher-vs-compact-student trade-off** and let executed evidence determine whether a simpler model is the better deployment choice.
