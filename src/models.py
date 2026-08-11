"""Model factory for required Part 2 baselines.

Hyperparameter optimization should be performed only on training/validation windows.
The defaults here are conservative starting points, not claimed optimal settings.
"""
from __future__ import annotations

from catboost import CatBoostClassifier
from lightgbm import LGBMClassifier
from sklearn.ensemble import RandomForestClassifier, StackingClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier


def build_model(name: str, seed: int = 20260811):
    name = name.lower()
    if name == "logistic_regression":
        return LogisticRegression(
            max_iter=3000,
            class_weight="balanced",
            solver="lbfgs",
            random_state=seed,
        )
    if name == "random_forest":
        return RandomForestClassifier(
            n_estimators=400,
            max_depth=None,
            min_samples_leaf=2,
            class_weight="balanced_subsample",
            n_jobs=-1,
            random_state=seed,
        )
    if name == "xgboost":
        return XGBClassifier(
            n_estimators=600,
            learning_rate=0.05,
            max_depth=6,
            subsample=0.85,
            colsample_bytree=0.85,
            eval_metric="logloss",
            n_jobs=-1,
            random_state=seed,
        )
    if name == "lightgbm":
        return LGBMClassifier(
            n_estimators=700,
            learning_rate=0.04,
            num_leaves=31,
            subsample=0.85,
            colsample_bytree=0.85,
            class_weight="balanced",
            random_state=seed,
            n_jobs=-1,
        )
    if name == "catboost":
        return CatBoostClassifier(
            iterations=700,
            learning_rate=0.04,
            depth=7,
            loss_function="Logloss",
            eval_metric="AUC",
            auto_class_weights="Balanced",
            random_seed=seed,
            verbose=False,
        )
    raise KeyError(f"Unknown model: {name}")


def build_stacking_ensemble(seed: int = 20260811):
    """Optional research ensemble; fit only after standalone baselines are frozen."""
    estimators = [
        ("xgb", build_model("xgboost", seed)),
        ("lgbm", build_model("lightgbm", seed)),
        ("cat", build_model("catboost", seed)),
    ]
    meta = LogisticRegression(max_iter=2000, class_weight="balanced", random_state=seed)
    return StackingClassifier(
        estimators=estimators,
        final_estimator=meta,
        stack_method="predict_proba",
        cv=5,
        n_jobs=-1,
        passthrough=False,
    )
