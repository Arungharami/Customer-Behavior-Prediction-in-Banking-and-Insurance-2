"""Prepare or publish a compact trained model bundle to Hugging Face Hub.

This script never creates model weights. It only packages an already executed model
from an accepted run. Authentication is taken from the local Hugging Face login/token.
"""
from __future__ import annotations

import argparse
import json
import shutil
import tempfile
from pathlib import Path

from huggingface_hub import HfApi, create_repo

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPO = "arun-gharami/customer-behavior-prediction-banking-insurance-part2"


def build_model_card(metadata: dict) -> str:
    return f"""---
license: mit
tags:
- tabular-classification
- finance
- banking
- insurance
- calibration
- model-stability
- explainable-ai
---

# Customer Behavior Prediction in Banking and Insurance - Part 2

## Model summary

This repository contains the compact practical model selected from the reproducible study:
**Beyond Static Accuracy: Temporal Stability, Probability Calibration, Explanation Stability, and Cost-Sensitive Customer Behavior Prediction in Banking and Insurance.**

The model is published only after the corresponding accepted research run passes all integrity gates.

## Intended use

Research and educational benchmarking of financial tabular prediction, calibration, drift monitoring, and explainability. It is **not** a production credit/insurance decision system and must not be used as a substitute for institutional validation, legal review, fairness assessment, or human oversight.

## Training provenance

- Dataset/task: {metadata.get('dataset', 'NOT RECORDED')}
- Model family: {metadata.get('model_family', 'NOT RECORDED')}
- Accepted run: {metadata.get('run_id', 'NOT RECORDED')}
- Git commit: {metadata.get('git_commit', 'NOT RECORDED')}
- Primary metric: {metadata.get('primary_metric', 'NOT RECORDED')}
- Metric value: {metadata.get('primary_metric_value', 'NOT RECORDED')}
- Calibration method: {metadata.get('calibration_method', 'NOT RECORDED')}

## Limitations

Performance can change under population, economic, policy, product, channel, and behavioral shifts. Users should reproduce the temporal, calibration, fairness, and drift analyses before relying on the model in a new environment.

## Reproducibility

Source code and artifact-generation protocol are maintained in the GitHub research repository. Raw Kaggle competition files are not redistributed in this model repository.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", type=Path, help="Accepted artifact run directory")
    parser.add_argument("--model-file", type=Path, help="Serialized compact model file")
    parser.add_argument("--metadata", type=Path, help="JSON file describing accepted model")
    parser.add_argument("--repo-id", default=DEFAULT_REPO)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.run_dir is None or args.model_file is None or args.metadata is None:
        raise SystemExit(
            "Provide --run-dir, --model-file, and --metadata from an executed accepted run. "
            "The script refuses to publish placeholder models."
        )

    if not args.model_file.exists() or not args.metadata.exists():
        raise SystemExit("Required executed model/metadata file does not exist.")

    metadata = json.loads(args.metadata.read_text(encoding="utf-8"))
    required = ["dataset", "model_family", "run_id", "git_commit", "primary_metric", "primary_metric_value"]
    missing = [k for k in required if metadata.get(k) in (None, "", "NOT EXECUTED")]
    if missing:
        raise SystemExit(f"Refusing publication; missing executed metadata fields: {missing}")

    with tempfile.TemporaryDirectory() as td:
        bundle = Path(td) / "model_bundle"
        bundle.mkdir()
        shutil.copy2(args.model_file, bundle / args.model_file.name)
        shutil.copy2(args.metadata, bundle / "metadata.json")
        (bundle / "README.md").write_text(build_model_card(metadata), encoding="utf-8")

        if args.dry_run:
            preview = ROOT / "artifacts" / "hf_export_preview"
            if preview.exists():
                shutil.rmtree(preview)
            shutil.copytree(bundle, preview)
            print(f"Dry run complete: {preview}")
            return

        create_repo(args.repo_id, repo_type="model", exist_ok=True)
        api = HfApi()
        api.upload_folder(
            repo_id=args.repo_id,
            repo_type="model",
            folder_path=str(bundle),
            commit_message="Publish accepted Part 2 compact model bundle",
        )
        print(f"Published model bundle to Hugging Face: {args.repo_id}")


if __name__ == "__main__":
    main()
