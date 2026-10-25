from __future__ import annotations

from collections import Counter

import pandas as pd


def extract_top_ngrams(texts: list[str], n: int = 2, top_k: int = 10) -> list[tuple[str, int]]:
    counts: Counter[str] = Counter()
    for text in texts:
        tokens = text.lower().split()
        if len(tokens) < n:
            continue
        for idx in range(len(tokens) - n + 1):
            gram = " ".join(tokens[idx : idx + n])
            counts[gram] += 1
    return counts.most_common(top_k)


def summarize_engagement_patterns(df: pd.DataFrame, label_col: str = "engagement_bait_label") -> dict[str, dict[str, object]]:
    result: dict[str, dict[str, object]] = {}
    if df is None or df.empty or label_col not in df.columns:
        return result

    pattern_maps = {
        "share": ["share", "repost", "retweet", "rt", "spread"],
        "comment": ["comment", "reply", "tag", "tagging", "mention"],
        "urgency": ["urgent", "now", "immediately", "before", "delete", "hide", "secret"],
        "social_pressure": ["must", "everyone", "traitors", "cowards", "only", "if you care"],
        "imperative": ["please", "share", "comment", "tag", "repost"],
    }

    for label, group in df.groupby(label_col, dropna=False):
        texts = group["text"].fillna("").astype(str).tolist()
        phrase_counts: dict[str, int] = {}
        for pattern_name, keywords in pattern_maps.items():
            total = 0
            for text in texts:
                lowered = text.lower()
                if any(keyword in lowered for keyword in keywords):
                    total += 1
            if total:
                phrase_counts[pattern_name] = total
        result[str(label)] = {
            "phrases": phrase_counts,
            "top_ngrams": extract_top_ngrams(texts, n=2, top_k=10),
        }

    return result
