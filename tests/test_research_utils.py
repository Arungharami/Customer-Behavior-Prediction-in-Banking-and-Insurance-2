import numpy as np
import pandas as pd

from src.drift import population_stability_index, shap_rank_stability
from src.evaluation import capacity_metrics, expected_calibration_error


def test_ece_perfect_probabilities_is_zero():
    y = np.array([0, 0, 1, 1])
    p = np.array([0.0, 0.0, 1.0, 1.0])
    assert expected_calibration_error(y, p, n_bins=2) == 0.0


def test_capacity_metrics_selects_high_scores():
    y = np.array([1, 0, 1, 0, 0])
    p = np.array([0.99, 0.10, 0.90, 0.20, 0.30])
    row = capacity_metrics(y, p, capacities=(0.4,)).iloc[0]
    assert row["n_selected"] == 2
    assert row["precision_at_capacity"] == 1.0
    assert row["recall_at_capacity"] == 1.0


def test_psi_identical_distribution_near_zero():
    x = np.arange(1, 101, dtype=float)
    assert abs(population_stability_index(x, x, bins=10)) < 1e-12


def test_shap_stability_identical_rankings():
    a = pd.Series({"a": 3.0, "b": 2.0, "c": 1.0})
    result = shap_rank_stability(a, a, top_k=(2,))
    assert abs(result["spearman_rank_correlation"] - 1.0) < 1e-12
    assert result["jaccard_top_2"] == 1.0
