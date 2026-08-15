"""Publication-grade evaluation helpers.

All functions operate on executed predictions. Nothing in this module invents or
fills missing results.
"""
from __future__ import annotations

import json
import math
import os
import tempfile
import time
from pathlib import Path
from typing import Callable, Iterable

import joblib
import numpy as np
import pandas as pd
from sklearn.calibration import calibration_curve
from sklearn.metrics import (
    average_precision_score,
    brier_score_loss,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.linear_model import LogisticRegression


def expected_calibration_error(y_true, y_prob, n_bins: int = 10) -> float:
    y_true = np.asarray(y_true)
    y_prob = np.asarray(y_prob)
    edges = np.linspace(0.0, 1.0, n_bins + 1)
    bins = np.digitize(y_prob, edges[1:-1], right=True)
    ece = 0.0
    n = len(y_true)
    for b in range(n_bins):
        mask = bins == b
        if not mask.any():
            continue
        conf = float(y_prob[mask].mean())
        acc = float(y_true[mask].mean())
        ece += (mask.sum() / n) * abs(acc - conf)
    return float(ece)


def threshold_metrics(y_true, y_prob, threshold: float = 0.5) -> dict:
    y_true = np.asarray(y_true)
    y_prob = np.asarray(y_prob)
    y_pred = (y_prob >= threshold).astype(int)
    return {
        "roc_auc": float(roc_auc_score(y_true, y_prob)),
        "average_precision": float(average_precision_score(y_true, y_prob)),
        "precision": float(precision_score(y_true, y_pred, zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, zero_division=0)),
        "f1": float(f1_score(y_true, y_pred, zero_division=0)),
        "brier_score": float(brier_score_loss(y_true, y_prob)),
        "ece_10": expected_calibration_error(y_true, y_prob, n_bins=10),
        **calibration_slope_intercept(y_true, y_prob),
    }


def calibration_slope_intercept(y_true, y_prob, eps: float = 1e-6) -> dict:
    """Fit outcome ~ logit(probability); ideal intercept=0 and slope=1."""
    y_true = np.asarray(y_true).astype(int)
    y_prob = np.clip(np.asarray(y_prob, dtype=float), eps, 1 - eps)
    if len(np.unique(y_true)) < 2:
        raise ValueError("Calibration slope requires both outcome classes.")
    logits = np.log(y_prob / (1 - y_prob)).reshape(-1, 1)
    model = LogisticRegression(C=1e6, solver="lbfgs", max_iter=2000).fit(logits, y_true)
    return {"calibration_intercept": float(model.intercept_[0]),
            "calibration_slope": float(model.coef_[0, 0])}


def cost_sensitive_metrics(y_true, y_prob, threshold: float, false_positive_cost: float,
                           false_negative_cost: float, true_positive_value: float = 0.0,
                           true_negative_value: float = 0.0) -> dict:
    """Return transparent confusion counts and normalized per-customer utility."""
    y_true = np.asarray(y_true).astype(int)
    y_pred = (np.asarray(y_prob) >= threshold).astype(int)
    tp = int(((y_true == 1) & (y_pred == 1)).sum())
    fp = int(((y_true == 0) & (y_pred == 1)).sum())
    fn = int(((y_true == 1) & (y_pred == 0)).sum())
    tn = int(((y_true == 0) & (y_pred == 0)).sum())
    utility = tp * true_positive_value + tn * true_negative_value - fp * false_positive_cost - fn * false_negative_cost
    return {"threshold": float(threshold), "tp": tp, "fp": fp, "fn": fn, "tn": tn,
            "total_utility": float(utility), "utility_per_customer": float(utility / len(y_true))}


def capacity_metrics(y_true, y_prob, capacities=(0.01, 0.05, 0.10, 0.15, 0.20)) -> pd.DataFrame:
    y_true = np.asarray(y_true).astype(int)
    y_prob = np.asarray(y_prob)
    order = np.argsort(-y_prob)
    base_rate = y_true.mean()
    rows = []
    for cap in capacities:
        k = max(1, int(math.ceil(len(y_true) * cap)))
        idx = order[:k]
        tp = int(y_true[idx].sum())
        precision = tp / k
        recall = tp / max(1, int(y_true.sum()))
        lift = precision / base_rate if base_rate > 0 else np.nan
        rows.append({
            "capacity": float(cap),
            "n_selected": int(k),
            "precision_at_capacity": float(precision),
            "recall_at_capacity": float(recall),
            "lift_at_capacity": float(lift),
        })
    return pd.DataFrame(rows)


def bootstrap_ci(
    y_true,
    y_prob,
    metric: Callable[[np.ndarray, np.ndarray], float],
    n_resamples: int = 1000,
    confidence: float = 0.95,
    seed: int = 20260811,
) -> dict:
    y_true = np.asarray(y_true)
    y_prob = np.asarray(y_prob)
    rng = np.random.default_rng(seed)
    values = []
    n = len(y_true)
    for _ in range(n_resamples):
        idx = rng.integers(0, n, size=n)
        ys = y_true[idx]
        ps = y_prob[idx]
        if len(np.unique(ys)) < 2:
            continue
        values.append(float(metric(ys, ps)))
    if not values:
        raise ValueError("No valid bootstrap samples; check target distribution.")
    alpha = 1.0 - confidence
    lo, hi = np.quantile(values, [alpha / 2, 1 - alpha / 2])
    return {
        "estimate": float(metric(y_true, y_prob)),
        "lower": float(lo),
        "upper": float(hi),
        "n_valid_resamples": len(values),
    }


def calibration_points(y_true, y_prob, n_bins: int = 10) -> pd.DataFrame:
    prob_true, prob_pred = calibration_curve(y_true, y_prob, n_bins=n_bins, strategy="quantile")
    return pd.DataFrame({"mean_predicted_probability": prob_pred, "observed_rate": prob_true})


def benchmark_inference(model, X, repeats: int = 20, warmup: int = 5) -> dict:
    sample = X
    for _ in range(warmup):
        model.predict_proba(sample)
    times_ms = []
    for _ in range(repeats):
        start = time.perf_counter()
        model.predict_proba(sample)
        times_ms.append((time.perf_counter() - start) * 1000.0)
    arr = np.asarray(times_ms)
    return {
        "batch_size": int(len(sample)),
        "p50_latency_ms": float(np.quantile(arr, 0.50)),
        "p95_latency_ms": float(np.quantile(arr, 0.95)),
        "mean_latency_ms": float(arr.mean()),
    }


def serialized_model_size_bytes(model) -> int:
    with tempfile.TemporaryDirectory() as td:
        path = Path(td) / "model.joblib"
        joblib.dump(model, path)
        return int(path.stat().st_size)


def save_json(data: dict, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
