from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, precision_recall_fscore_support
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC

from src.data.ingestion import map_engagement_label


def _binary_metrics(y_true: pd.Series, y_pred: np.ndarray) -> dict[str, Any]:
    precision, recall, f1, support = precision_recall_fscore_support(
        y_true, y_pred, average="binary", zero_division=0, labels=[0, 1]
    )
    support_value = int(support) if support is not None else 0
    return {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": float(precision),
        "recall": float(recall),
        "f1": float(f1),
        "support": support_value,
        "confusion_matrix": confusion_matrix(y_true, y_pred, labels=[0, 1]).tolist(),
    }


def evaluate_baseline_models(df: pd.DataFrame) -> dict[str, Any]:
    if df.empty or "text" not in df.columns or "engagement_bait_label" not in df.columns:
        return {"status": "missing_data", "message": "A dataset with text and engagement_bait_label is required."}

    prepared = df.copy()
    prepared["text"] = prepared["text"].fillna("").astype(str)
    prepared["engagement_bait_label"] = prepared["engagement_bait_label"].apply(map_engagement_label)
    prepared = prepared[prepared["text"].str.strip() != ""].copy()

    if prepared.empty:
        return {"status": "missing_data", "message": "No non-empty text rows were available for model training."}

    y = prepared["engagement_bait_label"].map({"engagement_bait": 1, "not_engagement_bait": 0})
    if y.nunique() < 2:
        return {"status": "insufficient_labels", "message": "At least one positive and one negative label are required."}
    if len(prepared) < 10:
        return {
            "status": "insufficient_data",
            "message": "At least 10 labeled rows are required for a stable train/validation/test split.",
        }

    X = prepared["text"].astype(str)
    X_train_val, X_test, y_train_val, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )
    X_train, X_val, y_train, y_val = train_test_split(
        X_train_val, y_train_val, test_size=0.25, stratify=y_train_val, random_state=42
    )

    models = {
        "logistic_regression": Pipeline([
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=1)),
            ("clf", LogisticRegression(max_iter=1000, class_weight="balanced")),
        ]),
        "linear_svm": Pipeline([
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=1)),
            ("clf", LinearSVC(class_weight="balanced")),
        ]),
    }

    results: dict[str, Any] = {"dataset_size": len(prepared), "random_seed": 42, "models": {}}
    for name, model in models.items():
        model.fit(X_train, y_train)
        val_pred = model.predict(X_val)
        test_pred = model.predict(X_test)
        results["models"][name] = {
            "validation": _binary_metrics(y_val, val_pred),
            "held_out_test": _binary_metrics(y_test, test_pred),
            "train_size": len(X_train),
            "validation_size": len(X_val),
            "test_size": len(X_test),
        }

    return results
