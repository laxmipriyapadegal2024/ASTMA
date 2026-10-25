import pandas as pd

from src.data.validation import validate_dataset


def test_missing_required_columns_fails():
    df = pd.DataFrame({"text": ["example"]})
    issues = validate_dataset(df)
    assert issues["errors"]


def test_duplicate_posts_are_reported():
    df = pd.DataFrame({"post_id": ["1", "1", "2"], "text": ["hello", "hello", "world"]})
    issues = validate_dataset(df)
    assert issues["duplicate_rows"] == 1


def test_valid_dataset_passes():
    df = pd.DataFrame(
        {
            "post_id": ["1", "2"],
            "text": ["Share this now!", "Officials met today."],
            "engagement_bait_label": [1, 0],
            "manipulation_labels": ["urgency_pressure", ""],
        }
    )
    issues = validate_dataset(df)
    assert not issues["errors"]
