# Research system, roadmap, and manuscript plan

This public plan is intentionally pre-results. No numeric performance finding has been executed or verified.

## Gap analysis

Implemented: deterministic configuration; provenance preflight; five model factories; temporal split manifest; discrimination, calibration, drift, explanation-stability, capacity, cost, bootstrap, latency, and size utilities; explicit evidence states; CI; and a fail-closed publication gate.

Blocked or incomplete: authorized benchmark data; dataset-specific relational joins and feature availability maps; executed leakage reports; tuned models; calibrated ensemble weights; SHAP artifacts; bootstrap runs; cost assumptions approved by a domain owner; verified tables/figures; and a results-bearing manuscript.

## Execution roadmap

1. Acquire datasets under their original terms and record file hashes, licenses, retrieval dates, schemas, and row counts.
2. Implement and test one adapter per dataset, including Home Credit relational aggregation and an explicit feature-availability ledger.
3. Freeze chronological train/calibration/test row assignments before inspecting comparative test performance.
4. Run leakage checks, missingness/drift summaries, and class prevalence by window.
5. Train Logistic Regression, Random Forest, XGBoost, LightGBM, and CatBoost with training-window-only tuning.
6. Calibrate eligible finalists on the calibration window and construct stability-aware weights without test access.
7. Execute windowed discrimination, calibration, drift, explanation, capacity, cost, uncertainty, and efficiency analyses.
8. Export the registered machine-readable tables and publication figures; verify checksums and claim lineage.
9. Run the publication gate, then write Results and Discussion from only accepted artifacts.
10. Deploy the accepted portal and perform desktop/mobile, accessibility, metadata, headers, links, and runtime checks.

## Manuscript outline

Abstract; Introduction and contributions; Literature Review; Data provenance and cohort construction; Frozen temporal protocol; Leakage-safe preprocessing; Models and calibration; Stability-aware ensemble; Metrics and operational utility; Uncertainty and efficiency; Results; Robustness and ablations; Discussion; Limitations; Ethics and compliance; Conclusion; References; Reproducibility supplement.

## Acceptance checklist

- Data and split manifests are immutable and checksum-backed.
- Test windows are untouched until all choices are frozen.
- All five baselines complete for every required dataset or a failure is documented.
- Calibration, drift, explanation stability, operational utility, uncertainty, and efficiency accompany discrimination.
- Every number and visual resolves to a registered artifact, run ID, commit, configuration, and environment.
- The portal renders numeric findings only for VERIFIED registry entries.
- Blind manuscript metadata and citations pass independent checks.
- CI, production build, live deployment, mobile layout, links, metadata, security headers, and runtime logs pass.

## Exact next experimental actions

Accept the relevant Kaggle competition terms; configure local Kaggle credentials; run `python scripts/download_kaggle_data.py --dataset all`; inspect and approve generated hashes; implement dataset adapters against the exact downloaded schemas; run `python -m src.pipeline --config config/research.yaml`; and preserve the first successful preflight run ID as the frozen protocol baseline.
