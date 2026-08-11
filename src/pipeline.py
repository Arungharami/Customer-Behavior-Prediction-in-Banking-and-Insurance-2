"""Fail-fast Part 2 experiment runner.

This module establishes a deterministic run, records provenance, validates local data,
and creates the accepted artifact contract. Dataset-specific model execution is added only
when the corresponding authorized files are present; the runner will never fabricate or
silently substitute missing data.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def sha256(path: Path, chunk_size: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(chunk_size):
            h.update(chunk)
    return h.hexdigest()


def git_commit() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip()
    except Exception:
        return "UNAVAILABLE"


def pip_freeze() -> str:
    try:
        return subprocess.check_output(
            [sys.executable, "-m", "pip", "freeze"], text=True
        )
    except Exception:
        return "pip freeze unavailable\n"


def collect_data_manifest(data_root: Path) -> dict:
    files = []
    if data_root.exists():
        for p in sorted(data_root.rglob("*")):
            if p.is_file():
                files.append(
                    {
                        "relative_path": str(p.relative_to(ROOT)),
                        "bytes": p.stat().st_size,
                        "sha256": sha256(p),
                    }
                )
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "root": str(data_root.relative_to(ROOT)) if data_root.is_relative_to(ROOT) else str(data_root),
        "files": files,
    }


def required_dataset_presence(config: dict, data_root: Path) -> dict[str, bool]:
    result = {}
    for name, meta in config.get("datasets", {}).items():
        if not meta.get("enabled", False):
            continue
        folder = data_root / name
        result[name] = folder.exists() and any(p.is_file() for p in folder.rglob("*"))
    return result


def initialize_run(config_path: Path, run_id: str | None = None) -> Path:
    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    if run_id is None:
        run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    artifact_root = ROOT / config["project"].get("artifact_root", "artifacts/runs")
    run_dir = artifact_root / run_id
    if run_dir.exists():
        raise SystemExit(f"Run directory already exists: {run_dir}")

    for sub in ["metrics", "figures", "tables", "models", "logs"]:
        (run_dir / sub).mkdir(parents=True, exist_ok=True)

    shutil.copy2(config_path, run_dir / "config_snapshot.yaml")
    commit = git_commit()
    (run_dir / "git_commit.txt").write_text(commit + "\n", encoding="utf-8")
    (run_dir / "environment.txt").write_text(
        f"python={sys.version}\nplatform={platform.platform()}\n\n{pip_freeze()}",
        encoding="utf-8",
    )

    data_root = ROOT / "data" / "kaggle"
    manifest = collect_data_manifest(data_root)
    manifest["dataset_presence"] = required_dataset_presence(config, data_root)
    (run_dir / "data_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8"
    )

    missing = [name for name, present in manifest["dataset_presence"].items() if not present]
    status = {
        "run_id": run_id,
        "git_commit": commit,
        "status": "BLOCKED_MISSING_DATA" if missing else "PREFLIGHT_PASSED",
        "missing_enabled_datasets": missing,
        "next_action": (
            "Run scripts/download_kaggle_data.py after authenticating Kaggle and accepting required competition rules."
            if missing
            else "Proceed with dataset adapters, leakage checks, frozen splits, and model execution."
        ),
    }
    (run_dir / "run_status.json").write_text(
        json.dumps(status, indent=2, sort_keys=True), encoding="utf-8"
    )

    print(json.dumps(status, indent=2))
    if missing:
        raise SystemExit(2)
    return run_dir


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=ROOT / "config" / "research.yaml")
    parser.add_argument("--run-id")
    args = parser.parse_args()
    initialize_run(args.config.resolve(), args.run_id)


if __name__ == "__main__":
    main()
