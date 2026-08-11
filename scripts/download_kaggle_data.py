"""Download authorized public benchmark data through the user's local Kaggle API credentials.

Raw data are written to data/kaggle/ and are gitignored. Competition rules must be
accepted by the user on Kaggle before protected competition files can be downloaded.
"""
from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "kaggle"

COMPETITIONS = {
    "home_credit_stability": "home-credit-credit-risk-model-stability",
    "porto_seguro": "porto-seguro-safe-driver-prediction",
    "ieee_cis_fraud": "ieee-fraud-detection",
}

DATASETS = {
    "bank_marketing": "adityamhaske/bank-marketing-dataset",
}


def run(cmd: list[str]) -> None:
    print("+", " ".join(cmd))
    subprocess.run(cmd, check=True)


def download_competition(name: str, slug: str) -> None:
    dest = OUT / name
    dest.mkdir(parents=True, exist_ok=True)
    run(["kaggle", "competitions", "download", "-c", slug, "-p", str(dest)])


def download_dataset(name: str, slug: str) -> None:
    dest = OUT / name
    dest.mkdir(parents=True, exist_ok=True)
    run(["kaggle", "datasets", "download", "-d", slug, "-p", str(dest), "--unzip"])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset",
        default="all",
        choices=["all", *COMPETITIONS.keys(), *DATASETS.keys()],
    )
    parser.add_argument(
        "--include-optional-fraud",
        action="store_true",
        help="Also download IEEE-CIS fraud data when --dataset all is used.",
    )
    args = parser.parse_args()

    OUT.mkdir(parents=True, exist_ok=True)

    try:
        if args.dataset == "all":
            for name, slug in COMPETITIONS.items():
                if name == "ieee_cis_fraud" and not args.include_optional_fraud:
                    continue
                download_competition(name, slug)
            for name, slug in DATASETS.items():
                download_dataset(name, slug)
        elif args.dataset in COMPETITIONS:
            download_competition(args.dataset, COMPETITIONS[args.dataset])
        else:
            download_dataset(args.dataset, DATASETS[args.dataset])
    except subprocess.CalledProcessError as exc:
        raise SystemExit(
            "Kaggle download failed. Confirm that the Kaggle API is authenticated and, "
            "for competitions, that you have manually accepted the competition rules. "
            f"Command exit code: {exc.returncode}"
        ) from exc


if __name__ == "__main__":
    main()
