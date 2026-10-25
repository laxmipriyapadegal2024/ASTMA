from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import MODELS_DIR
from src.models.evaluate import evaluate_baseline_models


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate the baseline engagement classifiers.")
    parser.add_argument("--input", required=True, help="Input CSV file path.")
    parser.add_argument("--output", default=str(MODELS_DIR / "engagement_model_metrics.json"), help="Output JSON metrics path.")
    args = parser.parse_args()

    df = pd.read_csv(Path(args.input))
    results = evaluate_baseline_models(df)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
