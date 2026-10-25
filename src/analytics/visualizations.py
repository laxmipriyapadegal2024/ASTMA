from __future__ import annotations

import pandas as pd


def summarize_counts(df: pd.DataFrame, column: str) -> pd.DataFrame:
    if column not in df.columns:
        return pd.DataFrame(columns=["label", "count"])
    counts = df[column].fillna("unknown").astype(str).value_counts().reset_index()
    counts.columns = ["label", "count"]
    return counts
