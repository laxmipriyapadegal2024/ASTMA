import pandas as pd

from src.data.ingestion import normalize_dataset_schema
from src.models.evaluate import evaluate_baseline_models


def test_normalize_dataset_schema_maps_labels():
    df = pd.DataFrame(
        {
            "text": ["Share this now!", "Officials met today."],
            "engagement_bait_label": ["1", "0"],
            "manipulation_labels": ["urgency_pressure;social_pressure", ""],
        }
    )
    normalized = normalize_dataset_schema(df, source_name="manual")
    assert normalized["engagement_bait_label"].tolist() == ["engagement_bait", "not_engagement_bait"]
    assert "urgency_pressure" in normalized["manipulation_labels"].iloc[0]


def test_evaluate_baseline_models_returns_two_models():
    rows = []
    for i in range(20):
        label = "engagement_bait" if i % 2 == 0 else "not_engagement_bait"
        text = "share now for everyone" if label == "engagement_bait" else "officials met to discuss trade"
        rows.append({"post_id": str(i), "text": text, "engagement_bait_label": label})
    result = evaluate_baseline_models(pd.DataFrame(rows))
    assert "models" in result
    assert set(result["models"]).issuperset({"logistic_regression", "linear_svm"})


def test_evaluate_baseline_models_rejects_tiny_datasets():
    rows = [
        {"post_id": "p1", "text": "Share this now!", "engagement_bait_label": "engagement_bait"},
        {"post_id": "p2", "text": "Officials met today.", "engagement_bait_label": "not_engagement_bait"},
        {"post_id": "p3", "text": "Please repost urgently.", "engagement_bait_label": "engagement_bait"},
        {"post_id": "p4", "text": "A government statement was released.", "engagement_bait_label": "not_engagement_bait"},
        {"post_id": "p5", "text": "Everyone must share this.", "engagement_bait_label": "engagement_bait"},
        {"post_id": "p6", "text": "Analysts discussed the policy update.", "engagement_bait_label": "not_engagement_bait"},
    ]
    result = evaluate_baseline_models(pd.DataFrame(rows))
    assert result["status"] == "insufficient_data"
    assert "At least 10 labeled rows" in result["message"]
