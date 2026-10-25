from __future__ import annotations

import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC

from src.config import MODELS_DIR
from src.data.ingestion import map_engagement_label


def train_baseline_models(df: pd.DataFrame, output_dir: str | Path | None = None) -> dict:
    output_dir = Path(output_dir) if output_dir else MODELS_DIR
    output_dir.mkdir(parents=True, exist_ok=True)

    if df.empty or "text" not in df.columns or "engagement_bait_label" not in df.columns:
        raise ValueError("A dataset with text and engagement_bait_label is required.")

    prepared = df.copy()
    prepared["text"] = prepared["text"].fillna("").astype(str)
    prepared["engagement_bait_label"] = prepared["engagement_bait_label"].apply(map_engagement_label)
    prepared = prepared[prepared["text"].str.strip() != ""].copy()

    y = prepared["engagement_bait_label"].map({"engagement_bait": 1, "not_engagement_bait": 0})
    X = prepared["text"].astype(str)

    if y.nunique() < 2:
        raise ValueError("The dataset needs both engagement_bait and not_engagement_bait examples.")

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    model_specs = {
        "logistic_regression": Pipeline([
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=1)),
            ("clf", LogisticRegression(max_iter=1000, class_weight="balanced")),
        ]),
        "linear_svm": Pipeline([
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=1)),
            ("clf", LinearSVC(class_weight="balanced")),
        ]),
    }

    artifact_summary = {
        "random_seed": 42,
        "train_size": len(X_train),
        "test_size": len(X_test),
        "class_distribution": {"0": int((y == 0).sum()), "1": int((y == 1).sum())},
        "models": {},
    }

    for name, model in model_specs.items():
        model.fit(X_train, y_train)
        joblib.dump(model, output_dir / f"{name}_model.joblib")
        artifact_summary["models"][name] = {
            "saved_path": str(output_dir / f"{name}_model.joblib"),
        }

    joblib.dump(model_specs["logistic_regression"], output_dir / "engagement_model.joblib")
    (output_dir / "engagement_model_metrics.json").write_text(json.dumps(artifact_summary, indent=2))
    return artifact_summary


def train_baseline_model(df: pd.DataFrame, output_dir: str | Path | None = None) -> dict:
    return train_baseline_models(df, output_dir=output_dir)
