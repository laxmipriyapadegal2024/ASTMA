from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.models.train import train_baseline_model


def main() -> None:
    parser = argparse.ArgumentParser(description="Train the baseline engagement classifier.")
    parser.add_argument("--input", required=True, help="Input CSV file path.")
    args = parser.parse_args()

    df = pd.read_csv(Path(args.input))
    metrics = train_baseline_model(df)
    print(metrics)


if __name__ == "__main__":
    main()
