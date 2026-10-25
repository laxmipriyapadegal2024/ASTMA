from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable

import pandas as pd

from src.data.validation import validate_dataset

DATASET_SOURCE_REGISTRY = [
    {
        "name": "LIAR",
        "source_url": "https://www.cs.uic.edu/~liub/FakeNews/index.html",
        "task": "political claim verification and truthfulness labels",
        "license": "Dataset-specific; review the source terms before reuse.",
        "intended_use": "Claim-level political text analysis and fact-check label mapping.",
        "notes": "Useful for claim text and verdict labels, but not a direct engagement-bait dataset.",
    },
    {
        "name": "FEVER",
        "source_url": "https://fever.ai/dataset/fever.html",
        "task": "evidence-based claim verification",
        "license": "Dataset-specific; review the source terms before reuse.",
        "intended_use": "Evidence retrieval and claim-status workflows.",
        "notes": "Not a social-media engagement-bait corpus and should not be treated as equivalent.",
    },
    {
        "name": "MultiFC",
        "source_url": "https://github.com/ENCASEH2021/MultiFC",
        "task": "multi-domain fact checking with claim, source, and verdict metadata",
        "license": "Dataset-specific; confirm the repository terms before use.",
        "intended_use": "Evidence and verdict mapping for claim verification research.",
        "notes": "Not a dedicated engagement-bait dataset.",
    },
    {
        "name": "Clickbait or engagement-bait corpora",
        "source_url": "https://huggingface.co/datasets or a repository-specific page",
        "task": "engagement prompting and clickbait detection",
        "license": "Dataset-specific; verify licensing before reuse.",
        "intended_use": "Only for engagement-bait research, not political-bias or misinformation detection.",
        "notes": "Clickbait labels are not equivalent to political engagement-bait labels.",
    },
]


def map_engagement_label(value: Any) -> str:
    if value is None or str(value).strip() == "":
        return "not_engagement_bait"
    normalized = str(value).strip().lower()
    mapping = {
        "1": "engagement_bait",
        "0": "not_engagement_bait",
        "true": "engagement_bait",
        "false": "not_engagement_bait",
        "engagement_bait": "engagement_bait",
        "not_engagement_bait": "not_engagement_bait",
        "bait": "engagement_bait",
        "non_bait": "not_engagement_bait",
    }
    return mapping.get(normalized, normalized)


def parse_manipulation_labels(value: Any) -> list[str]:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, set):
        return [str(item).strip() for item in value if str(item).strip()]
    text = str(value).strip()
    if not text:
        return []
    separators = [";", ",", "|"]
    for separator in separators:
        if separator in text:
            pieces = [piece.strip() for piece in text.split(separator)]
            return [piece for piece in pieces if piece]
    return [text]


def normalize_dataset_schema(df: pd.DataFrame, source_name: str = "manual") -> pd.DataFrame:
    if df is None:
        return pd.DataFrame()

    normalized = df.copy()
    rename_map = {
        "tweet": "text",
        "post": "text",
        "content": "text",
        "claim": "claim_text",
        "claim_text": "claim_text",
        "id": "post_id",
        "post_id": "post_id",
        "topic": "topic",
        "timestamp": "timestamp",
        "platform": "platform",
        "source_url": "source_url",
        "verdict": "claim_verdict",
        "claim_verdict": "claim_verdict",
        "evidence_source": "evidence_source",
    }
    normalized = normalized.rename(columns={key: value for key, value in rename_map.items() if key in normalized.columns})

    if "text" not in normalized.columns:
        if "post_text" in normalized.columns:
            normalized = normalized.rename(columns={"post_text": "text"})
        elif "message" in normalized.columns:
            normalized = normalized.rename(columns={"message": "text"})

    if "post_id" not in normalized.columns:
        normalized["post_id"] = [f"row_{idx}" for idx in range(len(normalized))]

    if "text" not in normalized.columns:
        raise ValueError("The dataset does not contain a usable text column.")

    normalized["text"] = normalized["text"].fillna("").astype(str).str.strip()
    if "post_id" in normalized.columns:
        normalized["post_id"] = normalized["post_id"].fillna("").astype(str)
    for col in ["timestamp", "topic", "platform", "source_url", "claim_text", "claim_verdict", "evidence_source"]:
        if col not in normalized.columns:
            normalized[col] = ""

    if "engagement_bait_label" in normalized.columns:
        normalized["engagement_bait_label"] = normalized["engagement_bait_label"].apply(map_engagement_label)
    else:
        normalized["engagement_bait_label"] = "not_engagement_bait"

    if "manipulation_labels" in normalized.columns:
        normalized["manipulation_labels"] = normalized["manipulation_labels"].apply(parse_manipulation_labels)
    else:
        normalized["manipulation_labels"] = [[] for _ in range(len(normalized))]

    if "source_name" not in normalized.columns:
        normalized["source_name"] = source_name

    normalized["dataset_source"] = source_name
    return normalized


def ingest_dataset(path: str | Path, *, source_name: str = "manual") -> dict[str, Any]:
    dataset_path = Path(path)
    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset not found: {dataset_path}")

    if dataset_path.suffix.lower() not in {".csv", ".tsv", ".txt"}:
        raise ValueError("This ingestion pipeline currently supports CSV/TSV/TXT tables.")

    df = pd.read_csv(dataset_path, sep="," if dataset_path.suffix.lower() == ".csv" else "\t")
    normalized = normalize_dataset_schema(df, source_name=source_name)
    validation = validate_dataset(normalized)
    duplicates_before = int(df.duplicated(subset=["text"], keep="first").sum()) if "text" in df.columns else 0
    normalized = normalized.drop_duplicates(subset=["text"], keep="first").reset_index(drop=True)

    return {
        "dataframe": normalized,
        "validation": validation,
        "source_name": source_name,
        "rows_loaded": len(df),
        "rows_after_deduplication": len(normalized),
        "duplicates_removed": duplicates_before,
        "dataset_registry": DATASET_SOURCE_REGISTRY,
    }


def list_known_datasets() -> list[dict[str, str]]:
    return [
        {
            "name": item["name"],
            "task": item["task"],
            "url": item["source_url"],
        }
        for item in DATASET_SOURCE_REGISTRY
    ]
