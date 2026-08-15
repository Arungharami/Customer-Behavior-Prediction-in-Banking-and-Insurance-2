"""Fail-fast publication integrity checks.

The gate validates that an accepted empirical run contains the canonical publication
artifacts and that a final manuscript has no unresolved evidence placeholders or legacy
figure/table numbering. It does not create or infer results.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Stage-1 frozen publication registry (2026-08-15).
REQUIRED_FIGURES = [f"figure_{i:02d}_" for i in range(1, 10)]
REQUIRED_TABLES = [f"table_{i:02d}_" for i in range(1, 12)]

# All of these are acceptable during research execution but prohibited in the final
# submission-bearing manuscript passed to this gate.
PLACEHOLDERS = [
    "NOT EXECUTED",
    "NOT_EXECUTED",
    "NOT MEASURED",
    "NOT_MEASURED",
    "INSUFFICIENT EVIDENCE",
    "INSUFFICIENT_EVIDENCE",
    "REQUIRES VALIDATION",
    "REQUIRES_VALIDATION",
    "[RESULT]",
    "[RESULTS]",
    "[INSERT RESULT]",
    "[INSERT RESULTS]",
    "[TBD]",
    "TODO_RESULT",
    "PRE-RESULTS",
    "DO NOT SUBMIT",
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

    for required in [
        "config_snapshot.yaml",
        "environment.txt",
        "git_commit.txt",
        "data_manifest.json",
        "evidence_registry.json",
        "run_status.json",
    ]:
        if not (run_dir / required).exists():
            failures.append(f"missing run metadata: {required}")

    registry_path = run_dir / "evidence_registry.json"
    if registry_path.exists():
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
        non_verified = [
            item["id"]
            for item in registry.get("items", [])
            if item.get("id") != "preflight" and item.get("state") != "VERIFIED"
        ]
        if non_verified:
            failures.append(
                f"evidence registry contains non-verified publication items: {non_verified}"
            )

    figures = run_dir / "figures"
    tables = run_dir / "tables"
    for prefix in REQUIRED_FIGURES:
        if len(find_prefix(figures, prefix)) != 1:
            failures.append(f"expected exactly one figure artifact matching {prefix}*")
    for prefix in REQUIRED_TABLES:
        if len(find_prefix(tables, prefix)) != 1:
            failures.append(f"expected exactly one table artifact matching {prefix}*")

    if args.manuscript_source:
        if not args.manuscript_source.exists():
            failures.append(f"manuscript source does not exist: {args.manuscript_source}")
        else:
            text = args.manuscript_source.read_text(encoding="utf-8", errors="ignore")
            for token in PLACEHOLDERS:
                if token.lower() in text.lower():
                    failures.append(f"manuscript contains unresolved evidence token: {token}")

            legacy_figure_patterns = re.findall(
                r"Figure\s*-?\s*\d+\.\d+", text, flags=re.I
            )
            legacy_table_patterns = re.findall(
                r"Table\s*-?\s*\d+\.\d+", text, flags=re.I
            )
            if legacy_figure_patterns:
                failures.append(
                    "legacy section-style figure numbering found: "
                    f"{legacy_figure_patterns[:5]}"
                )
            if legacy_table_patterns:
                failures.append(
                    "legacy section-style table numbering found: "
                    f"{legacy_table_patterns[:5]}"
                )

            # Basic cross-reference presence check. A final manuscript should cite each
            # canonical item at least once; deeper caption/source validation is handled by
            # the claim-evidence audit.
            for i in range(1, 10):
                if re.search(rf"\bFigure\s+{i}\b", text, flags=re.I) is None:
                    failures.append(f"manuscript does not cite Figure {i}")
            for i in range(1, 12):
                if re.search(rf"\bTable\s+{i}\b", text, flags=re.I) is None:
                    failures.append(f"manuscript does not cite Table {i}")

    if failures:
        print("RESEARCH GATE: FAILED")
        for failure in failures:
            print("-", failure)
        raise SystemExit(1)

    latest = ROOT / "artifacts" / "latest.json"
    latest.parent.mkdir(parents=True, exist_ok=True)
    latest.write_text(
        json.dumps({"accepted_run": str(run_dir)}, indent=2), encoding="utf-8"
    )
    print("RESEARCH GATE: PASSED")
    print(f"Accepted run pointer written to {latest}")


if __name__ == "__main__":
    main()
