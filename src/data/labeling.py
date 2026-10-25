from __future__ import annotations

from typing import Any


def normalize_label(value: Any) -> str:
    if value is None:
        return "unknown"
    label = str(value).strip().lower()
    mapping = {
        "1": "engagement_bait",
        "0": "not_engagement_bait",
        "engagement_bait": "engagement_bait",
        "not_engagement_bait": "not_engagement_bait",
    }
    return mapping.get(label, label)
