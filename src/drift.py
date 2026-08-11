"""Drift and explanation-stability metrics used by the Part 2 study."""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.stats import spearmanr, wasserstein_distance


def population_stability_index(reference, current, bins: int = 10, eps: float = 1e-6) -> float:
    """Compute PSI using quantile bins estimated from the reference sample."""
    reference = np.asarray(reference, dtype=float)
    current = np.asarray(current, dtype=float)
    reference = reference[np.isfinite(reference)]
    current = current[np.isfinite(current)]
    if len(reference) == 0 or len(current) == 0:
        return float("nan")
    edges = np.unique(np.quantile(reference, np.linspace(0, 1, bins + 1)))
    if len(edges) < 3:
        return 0.0
    edges[0] = -np.inf
    edges[-1] = np.inf
    ref_counts, _ = np.histogram(reference, bins=edges)
    cur_counts, _ = np.histogram(current, bins=edges)
    ref_pct = np.clip(ref_counts / max(1, ref_counts.sum()), eps, None)
    cur_pct = np.clip(cur_counts / max(1, cur_counts.sum()), eps, None)
    return float(np.sum((cur_pct - ref_pct) * np.log(cur_pct / ref_pct)))


def numeric_drift_table(reference_df: pd.DataFrame, current_df: pd.DataFrame, columns=None) -> pd.DataFrame:
    if columns is None:
        columns = sorted(set(reference_df.select_dtypes(include="number").columns) & set(current_df.columns))
    rows = []
    for col in columns:
        ref = reference_df[col].dropna().to_numpy()
        cur = current_df[col].dropna().to_numpy()
        if len(ref) == 0 or len(cur) == 0:
            continue
        rows.append({
            "feature": col,
            "psi": population_stability_index(ref, cur),
            "wasserstein": float(wasserstein_distance(ref, cur)),
            "reference_mean": float(np.mean(ref)),
            "current_mean": float(np.mean(cur)),
        })
    return pd.DataFrame(rows).sort_values("psi", ascending=False).reset_index(drop=True)


def shap_rank_stability(early_mean_abs: pd.Series, late_mean_abs: pd.Series, top_k=(10, 20)) -> dict:
    """Compare global mean-|SHAP| feature rankings between two windows."""
    common = early_mean_abs.index.intersection(late_mean_abs.index)
    if len(common) < 2:
        raise ValueError("At least two common features are required for rank stability.")
    early = early_mean_abs.loc[common].sort_values(ascending=False)
    late = late_mean_abs.loc[common].sort_values(ascending=False)
    early_rank = early.rank(ascending=False, method="average")
    late_rank = late.rank(ascending=False, method="average")
    rho = float(spearmanr(early_rank, late_rank).statistic)
    result = {"spearman_rank_correlation": rho}
    for k in top_k:
        e = set(early.head(k).index)
        l = set(late.head(k).index)
        union = e | l
        result[f"jaccard_top_{k}"] = float(len(e & l) / len(union)) if union else 1.0
    return result


def metric_slope_by_time(time_index, metric_values) -> float:
    x = np.asarray(time_index, dtype=float)
    y = np.asarray(metric_values, dtype=float)
    mask = np.isfinite(x) & np.isfinite(y)
    if mask.sum() < 2:
        return float("nan")
    return float(np.polyfit(x[mask], y[mask], deg=1)[0])
