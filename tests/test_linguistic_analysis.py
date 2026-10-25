import pandas as pd

from src.features.ngrams import summarize_engagement_patterns


def test_summarize_engagement_patterns_groups_by_label():
    df = pd.DataFrame(
        {
            "text": ["share now comment below", "share this widely", "officials met today"],
            "engagement_bait_label": ["engagement_bait", "engagement_bait", "not_engagement_bait"],
        }
    )
    summary = summarize_engagement_patterns(df)
    assert "engagement_bait" in summary
    assert "not_engagement_bait" in summary
    assert any(keyword in summary["engagement_bait"]["phrases"] for keyword in ["share", "comment"])
