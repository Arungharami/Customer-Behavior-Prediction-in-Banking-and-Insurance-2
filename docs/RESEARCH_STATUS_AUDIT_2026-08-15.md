# Stage 0 — Repository and Manuscript Audit

**Audit date:** 2026-08-15  
**Repository:** `Arungharami/Customer-Behavior-Prediction-in-Banking-and-Insurance-2`  
**Audit branch:** `agent/final-publication-audit-20260815`  
**Scientific rule:** No empirical result may enter the manuscript unless it is traceable to an executed, versioned artifact.

## Executive status

The repository currently provides a sound **protocol and reproducibility scaffold**, but it does **not** yet contain an accepted empirical run. The public status file reports zero executed benchmark studies and zero verified empirical results. The manuscript available to the project is a pre-results research-execution draft and must remain non-submittable until the evidence gates pass.

**Current overall state: `BLOCKED_BEFORE_STAGE_2/3 EXECUTION`**

Primary blockers:

1. No authorized benchmark data are present in the repository/runtime.
2. Dataset-specific adapters, feature-availability audits, and leakage tests are not complete.
3. Rolling-origin training/evaluation has not been executed.
4. Calibration, SHAP stability, cost-sensitive analysis, ablations, and statistical synthesis have not been executed end-to-end.
5. No accepted figures/tables or claim-evidence matrix exist.
6. The Part 1 institutional 120,000-customer data described by the draft are not present in this repository, so Part 2 cannot rely on that dataset unless it is independently re-authorized and reconstructed.

## Research-status matrix

| Component | Required | Existing | Verified | Missing | Next Action |
|---|---:|---|---|---|---|
| Manuscript | Yes | Pre-results execution draft exists outside public repo; `paper/README.md` deliberately excludes it | Partial | Final evidence-backed Results/Discussion/Abstract/Conclusion | Keep locked until publication gate passes |
| Research protocol | Yes | `config/research.yaml`, `docs/MASTER_RESEARCH_PROMPT.md`, `docs/PAPER_BLUEPRINT.md` | Yes, as protocol | Final alignment to master prompt | Freeze in Stage 1 |
| Datasets | Yes | Dataset roles/slugs configured | No | Raw/authorized data and hashes | Obtain legally/technically authorized files |
| Dataset licenses/rules | Yes | Restrictions noted qualitatively | No | Per-dataset license/rules/access evidence | Create dataset cards and provenance records |
| Dataset manifests | Yes | `src/pipeline.py` can hash present local files | No empirical manifest | Actual file hashes/versions/access dates | Run preflight after data acquisition |
| Notebooks | Helpful | `notebooks/00_colab_bootstrap.ipynb` | Partial | End-to-end research notebook or scripted run | Keep notebook exploratory; use source pipeline for final results |
| Python source | Yes | `src/protocol.py`, `models.py`, `evaluation.py`, `drift.py`, `pipeline.py`, `registry.py` | Partial | Dataset adapters, preprocessing package, calibration runner, SHAP runner, decision runner, visualization runner | Implement only after data schema is known |
| Preprocessing | Yes | Config defines train-only fitting, median/mode imputation, unknown-category handling | Protocol only | Dataset-specific implementation and tests | Build sklearn-compatible leakage-safe pipelines |
| Feature engineering | Yes | Conceptual only | No | Executable feature builders and provenance | Implement per dataset; avoid unsupported cross-dataset feature assumptions |
| Feature availability audit | Yes | Bank Marketing `duration` exclusion configured | Partial | Full per-feature audit CSV | Populate `docs/feature_availability_audit.csv` from actual schemas |
| Labels | Yes | Target names configured | Partial | Verified label semantics/horizons per dataset | Validate against original dataset documentation |
| 90-day horizon | Preferred, not universal | Manuscript concept | No | Evidence that each dataset supports it | Use only where reconstructible; otherwise report task-native horizon |
| Temporal splits | Yes | `src/protocol.py` supports ordered train/calibration/test partition | Protocol verified | Rolling-origin folds and dataset-specific time boundaries | Implement forward-chaining fold generator |
| Random comparison split | Optional scientific comparator | Configured | Protocol only | Executed paired comparison | Run only when methodologically valid |
| Logistic Regression | Yes | Factory implemented | Code present | Training/evaluation artifacts | Execute on frozen folds |
| Random Forest | Yes | Factory implemented | Code present | Training/evaluation artifacts | Execute on frozen folds |
| XGBoost | Yes | Factory implemented | Code present | Training/evaluation artifacts | Execute on frozen folds |
| LightGBM | Optional advanced baseline | Factory implemented | Code present | Training/evaluation artifacts | Execute after minimum required baselines |
| CatBoost | Optional advanced baseline | Factory implemented | Code present | Training/evaluation artifacts | Execute after minimum required baselines |
| Prior stacked ensemble | Yes if reproducible | Stacking factory exists, but differs from Part 1 because it stacks XGB+LightGBM+CatBoost | No | A faithful Part 1-compatible stack or explicit methodological redefinition | Decide and document before execution |
| Hyperparameters | Yes | Conservative defaults | No | Time-safe search protocol and selected values | Freeze search spaces before final test use |
| Random seeds | Yes | Project seed `20260811` | Protocol verified | Per-run seed manifest | Record in experiment manifest |
| ROC-AUC / PR-AUC / P/R/F1 | Yes | Implemented | Utility-level only | Fold-level executed outputs | Execute and save |
| Specificity / sensitivity | Requested | Recall covers sensitivity; specificity absent | No | Explicit specificity metric | Add before execution |
| Brier / ECE / calibration slope-intercept | Yes | Implemented in evaluation utilities | Utility-level only | Fold/window calibration experiments | Execute and save |
| Log loss | Requested | Not implemented | No | Metric implementation | Add before execution |
| Calibration curves | Yes | Point-generation helper exists | Utility-level only | Calibrator fitting/evaluation scripts and figures | Implement Platt/isotonic using calibration folds only |
| Drift analysis | Yes | Numeric PSI/Wasserstein and performance slope helpers | Partial | KS/JS where appropriate, categorical drift, prediction drift, calibration drift runner | Implement dataset-aware drift suite |
| SHAP | Yes | No execution module in `src/` | No | SHAP computation, artifact saving, background/sample protocol | Implement after models/folds are frozen |
| Explanation stability | Yes | Spearman + Jaccard utility exists | Utility-level only | Rank displacement/sign consistency/fold outputs | Implement and execute |
| Cost-sensitive analysis | Yes | Confusion-cost and capacity utilities exist | Utility-level only | Threshold-selection protocol, scenario grid runner, figures/tables | Implement and execute using calibration window only |
| Complexity benchmarking | Yes | Inference latency and model-size helpers exist | Partial | Training wall time, peak memory, throughput, hardware/environment record | Implement and execute on one fixed environment |
| Statistical tests | Conditional | Bootstrap CI helper exists | Partial | Paired/grouped bootstrap, multiple-comparison control, dependence-aware policy | Implement based on actual fold/customer structure |
| Ablations | Yes | Six ablations configured | Protocol only | Executed experiments | Run only after core pipeline succeeds |
| Figures | Yes | Registry/protocol only | No | Executed Figures 1–9/10 with source-data artifacts | Generate automatically after experiments |
| Tables | Yes | Registry/protocol only | No | Executed publication tables with source CSVs | Generate automatically after experiments |
| Saved models | Yes | HF packaging script only | No | Fitted accepted model(s) | Save only from accepted run |
| Experiment manifests | Yes | Preflight manifest machinery exists | Partial | Full experiment-level manifest | Extend per model/fold/run |
| Environment files | Yes | `requirements.txt`; runtime `pip freeze` captured by preflight | Partial | Lockfile/clean-environment validation | Add deterministic Python lock once environment is stable |
| README | Yes | Strong protocol/reproduction overview | Yes for protocol | Update with actual accepted run after execution | Keep claims status-aware |
| CI/tests | Yes | Research integrity workflow + one utility test file | Partial | Dataset leakage tests, split tests, artifact-schema tests, claim audit tests | Expand before empirical acceptance |
| Citations | Yes | Draft/protocol contain candidate literature | No full audit | DOI/title/authors/year verification matrix | Verify from primary sources before final manuscript |
| Supplementary material | Yes | Plans only | No | Dataset cards, experiment manifests, claim matrix, additional fold tables | Generate from accepted run |
| Hugging Face | Optional | Packaging script/plan exists | No model | Accepted compact model and verified license | Publish only after all gates and license checks |
| Kaggle reproducibility | Optional | Downloader/bootstrap design exists | No package | Dataset metadata + reproducible notebook | Prepare only where rules permit |

## Code-level findings

### Temporal protocol

`src/protocol.py` correctly enforces ordered train → calibration → test partitions and can write a hashed split manifest. It does **not** yet implement the rolling-origin sequence required by the final master protocol.

### Model factories

`src/models.py` includes Logistic Regression, Random Forest, XGBoost, LightGBM, CatBoost, and a stacking classifier. Important: the current stack uses XGBoost + LightGBM + CatBoost, whereas the Part 1 paper described Random Forest + XGBoost feeding a logistic meta-learner. The final paper must either reproduce the Part 1 stack faithfully or explicitly define the new ensemble as a new Part 2 method.

### Evaluation utilities

`src/evaluation.py` implements ROC-AUC, average precision, precision, recall, F1, Brier score, ECE, calibration slope/intercept, capacity metrics, cost-sensitive utility, ordinary bootstrap CIs, inference timing, and serialized model size. Missing or incomplete for the master protocol: specificity, log loss, grouped/paired resampling, training-time wrapper, peak-memory measurement, explicit calibrator training, and fold-level orchestration.

### Drift utilities

`src/drift.py` implements numeric PSI, Wasserstein distance, SHAP rank Spearman correlation, top-k Jaccard overlap, and metric slope. Missing: categorical drift, KS/JS selection by data type, prediction-distribution drift orchestration, calibration drift orchestration, rank displacement, sign consistency, and source-data artifact generation.

### Publication gate

`scripts/research_gate.py` is appropriately fail-fast, but it currently expects Figures 1–10 and Tables 1–9. The user’s latest master protocol proposes a 9-figure / 11-table candidate sequence. Stage 1 must freeze one canonical registry and update the gate atomically before empirical outputs are produced.

## Manuscript findings

The current manuscript is scientifically useful as a pre-results protocol, but it cannot be called publication-ready because:

- it contains no executed Part 2 Results;
- it assumes a de-identified 120,000-customer institutional environment that is not present in the repository;
- its common 90-day horizon must be validated per actual dataset rather than imposed where impossible;
- its references require independent bibliographic verification;
- the final paper must distinguish source-derived facts, executed results, scenario assumptions, and governance interpretation.

## Stage 0 decision

**Stage 0: PASS for protocol audit, FAIL for empirical readiness.**

The project may proceed to **Stage 1 — research-question and contribution freeze**, and to **Stage 2 — dataset provenance/licensing work**. It may **not** proceed to final Results writing.
