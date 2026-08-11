# Figure and Table Registry

This registry is the single source of truth for manuscript numbering. Never create a manuscript figure/table without registering it here first.

## Figures

| No. | Canonical filename | Purpose | Backing artifact |
|---|---|---|---|
| Figure 1 | `figure_01_research_framework.png` | End-to-end trustworthy prediction framework | generated from pipeline architecture |
| Figure 2 | `figure_02_temporal_design.png` | Leakage-safe train/calibration/test timeline | split manifest |
| Figure 3 | `figure_03_dataset_characteristics.png` | Dataset sizes, targets, imbalance and time coverage | data manifest |
| Figure 4 | `figure_04_discrimination.png` | ROC-AUC/PR-AUC comparison | main metrics |
| Figure 5 | `figure_05_temporal_stability.png` | Performance by time window and stability slope | temporal metrics |
| Figure 6 | `figure_06_calibration.png` | Reliability diagrams raw vs calibrated | calibration metrics |
| Figure 7 | `figure_07_drift_dashboard.png` | PSI and feature/score drift | drift metrics |
| Figure 8 | `figure_08_shap_stability.png` | Early vs late SHAP stability | SHAP artifacts |
| Figure 9 | `figure_09_pareto_frontier.png` | Accuracy-calibration-stability-efficiency Pareto view | performance + complexity |
| Figure 10 | `figure_10_net_benefit.png` | Cost/capacity net-benefit sensitivity | operational simulation |

## Tables

| No. | Canonical filename | Purpose |
|---|---|---|
| Table 1 | `table_01_dataset_provenance.csv` | Dataset provenance, task, sample size, time field, target, rules/license |
| Table 2 | `table_02_features_leakage_controls.csv` | Feature families and leakage controls |
| Table 3 | `table_03_models_hyperparameters.csv` | Models, search spaces and selected hyperparameters |
| Table 4 | `table_04_main_performance.csv` | Main holdout metrics with 95% CIs |
| Table 5 | `table_05_stability_calibration.csv` | Temporal stability and calibration metrics |
| Table 6 | `table_06_explanation_stability.csv` | SHAP rank/Jaccard stability |
| Table 7 | `table_07_complexity.csv` | Train time, latency, memory, serialized size |
| Table 8 | `table_08_operational_value.csv` | Cost-sensitive/capacity outcomes |
| Table 9 | `table_09_ablations.csv` | Required ablations |

## Caption rules

- Captions must use exactly `Figure N. ...` and `Table N. ...`.
- Every figure/table must be cited in the narrative before or adjacent to its placement.
- Never use legacy labels such as `Figure 4.9`, `Figure-3.6`, or section-prefixed numbering.
- Cross-references must be globally sequential from Figure 1 through Figure 10 and Table 1 through Table 9.
- A conceptual figure must be clearly labeled conceptual; empirical figures must be generated from accepted-run artifacts.
