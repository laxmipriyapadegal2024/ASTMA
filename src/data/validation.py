from __future__ import annotations

from typing import Any

import pandas as pd

REQUIRED_COLUMNS = ["post_id", "text", "engagement_bait_label"]


def validate_dataset(df: pd.DataFrame) -> dict[str, Any]:
    if df is None or df.empty:
        return {"errors": ["Dataset is empty."], "warnings": [], "duplicate_rows": 0, "valid": False}

    errors: list[str] = []
    warnings: list[str] = []

    missing = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing:
        errors.append(f"Missing required columns: {', '.join(missing)}")

    if "text" in df.columns:
        blank_rows = int(df["text"].fillna("").astype(str).str.strip().eq("").sum())
        if blank_rows:
            warnings.append(f"{blank_rows} empty text rows were found.")

    if "timestamp" in df.columns:
        invalid_timestamps = 0
        for ts in df["timestamp"].dropna():
            try:
                pd.to_datetime(ts)
            except (TypeError, ValueError):
                invalid_timestamps += 1
        if invalid_timestamps:
            warnings.append(f"{invalid_timestamps} invalid timestamps were found.")

    duplicates = int(df.duplicated(subset=["text"], keep="first").sum()) if "text" in df.columns else 0
    duplicate_rows = duplicates

    if "engagement_bait_label" in df.columns:
        valid_labels = {0, 1, "0", "1", "engagement_bait", "not_engagement_bait"}
        bad_labels = df["engagement_bait_label"].astype(str).isin([str(v) for v in valid_labels])
        invalid_values = int((~bad_labels).sum())
        if invalid_values:
            warnings.append(f"{invalid_values} invalid engagement labels were found.")

    if "manipulation_labels" in df.columns:
        nan_count = int(df["manipulation_labels"].isna().sum())
        if nan_count:
            warnings.append(f"{nan_count} missing manipulation labels were found.")

    if "engagement_bait_label" in df.columns:
        label_counts = df["engagement_bait_label"].astype(str).value_counts(dropna=False)
        if label_counts.empty:
            warnings.append("No engagement labels were found after validation.")

    return {
        "errors": errors,
        "warnings": warnings,
        "duplicate_rows": duplicate_rows,
        "valid": not errors,
        "class_distribution": df["engagement_bait_label"].astype(str).value_counts(dropna=False).to_dict() if "engagement_bait_label" in df.columns else {},
    }
