"""Frozen, leakage-safe temporal protocol primitives."""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class TemporalSplit:
    train: np.ndarray
    calibration: np.ndarray
    test: np.ndarray


def temporal_split_indices(frame: pd.DataFrame, time_column: str, train_fraction: float = 0.60,
                           calibration_fraction: float = 0.20) -> TemporalSplit:
    if time_column not in frame:
        raise KeyError(f"Required time column is missing: {time_column}")
    if frame[time_column].isna().any():
        raise ValueError(f"Time column contains missing values: {time_column}")
    if not 0 < train_fraction < 1 or not 0 < calibration_fraction < 1:
        raise ValueError("Split fractions must be between zero and one.")
    if train_fraction + calibration_fraction >= 1:
        raise ValueError("Train and calibration fractions must leave a test partition.")
    order = frame.sort_values(time_column, kind="stable").index.to_numpy()
    train_end = int(np.floor(len(order) * train_fraction))
    calibration_end = int(np.floor(len(order) * (train_fraction + calibration_fraction)))
    if train_end == 0 or calibration_end == train_end or calibration_end == len(order):
        raise ValueError("Dataset is too small for three non-empty temporal partitions.")
    return TemporalSplit(order[:train_end], order[train_end:calibration_end], order[calibration_end:])


def assert_temporal_order(frame: pd.DataFrame, time_column: str, split: TemporalSplit) -> None:
    if (frame.loc[split.train, time_column].max() > frame.loc[split.calibration, time_column].min()
            or frame.loc[split.calibration, time_column].max() > frame.loc[split.test, time_column].min()):
        raise AssertionError("Temporal partitions overlap or are out of order.")


def write_split_manifest(path: str | Path, dataset: str, time_column: str,
                         split: TemporalSplit, seed: int) -> None:
    payload = {"schema_version": 1, "dataset": dataset, "time_column": time_column, "seed": seed,
               "partitions": {"train": split.train.tolist(), "calibration": split.calibration.tolist(),
                              "test": split.test.tolist()}}
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
