"""Fail-fast publication integrity checks.

The script validates that the accepted run contains the expected figure/table files and
that no obvious placeholder tokens remain in manuscript sources.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FIGURES = [f"figure_{i:02d}_" for i in range(1, 11)]
REQUIRED_TABLES = [f"table_{i:02d}_" for i in range(1, 10)]
PLACEHOLDERS = [
    "NOT EXECUTED",
    "[RESULT]",
    "[INSERT RESULT]",
    "[TBD]",
    "TODO_RESULT",
]


def find_prefix(directory: Path, prefix: str) -> list[Path]:
    if not directory.exists():
        return []
    return [p for p in directory.iterdir() if p.name.startswith(prefix)]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--manuscript-source", type=Path)
    args = parser.parse_args()

    run_dir = args.run_dir.resolve()
    failures: list[str] = []

    for required in ["config_snapshot.yaml", "environment.txt", "git_commit.txt", "data_manifest.json"]:
        if not (run_dir / required).exists():
            failures.append(f"missing run metadata: {required}")

    figures = run_dir / "figures"
    tables = run_dir / "tables"
    for prefix in REQUIRED_FIGURES:
        if len(find_prefix(figures, prefix)) != 1:
            failures.append(f"expected exactly one figure artifact matching {prefix}*")
    for prefix in REQUIRED_TABLES:
        if len(find_prefix(tables, prefix)) != 1:
            failures.append(f"expected exactly one table artifact matching {prefix}*")

    if args.manuscript_source:
        text = args.manuscript_source.read_text(encoding="utf-8", errors="ignore")
        for token in PLACEHOLDERS:
            if token.lower() in text.lower():
                failures.append(f"manuscript contains placeholder token: {token}")
        legacy_figure_patterns = re.findall(r"Figure\s*-?\s*\d+\.\d+", text, flags=re.I)
        if legacy_figure_patterns:
            failures.append(f"legacy section-style figure numbering found: {legacy_figure_patterns[:5]}")

    if failures:
        print("RESEARCH GATE: FAILED")
        for failure in failures:
            print("-", failure)
        raise SystemExit(1)

    latest = ROOT / "artifacts" / "latest.json"
    latest.parent.mkdir(parents=True, exist_ok=True)
    latest.write_text(json.dumps({"accepted_run": str(run_dir)}, indent=2), encoding="utf-8")
    print("RESEARCH GATE: PASSED")
    print(f"Accepted run pointer written to {latest}")


if __name__ == "__main__":
    main()
