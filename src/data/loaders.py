from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.config import SAMPLE_DATA_DIR


def load_sample_dataset(path: str | Path | None = None) -> pd.DataFrame:
    dataset_path = Path(path) if path else SAMPLE_DATA_DIR / "sample_posts.csv"
    if not dataset_path.exists():
        return pd.DataFrame(columns=["post_id", "text", "engagement_bait_label", "manipulation_labels", "topic"]) 
    return pd.read_csv(dataset_path)


def load_processed_dataset(path: str | Path | None = None) -> pd.DataFrame:
    if path is None:
        return load_sample_dataset()
    dataset_path = Path(path)
    if not dataset_path.exists():
        return pd.DataFrame(columns=["post_id", "text", "engagement_bait_label", "manipulation_labels", "topic"]) 
    return pd.read_csv(dataset_path)
