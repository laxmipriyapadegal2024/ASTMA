from src.models.manipulation_classifier import ManipulationDetector


def test_multiple_indicators_detected():
    detector = ManipulationDetector()
    result = detector.predict("Share now before they hide this! The elite are plotting against us.")
    labels = result["labels"]
    assert "urgency_pressure" in labels
    assert "social_pressure" in labels


def test_neutral_reporting_is_not_manipulative():
    detector = ManipulationDetector()
    result = detector.predict("Officials said a trade restriction took effect this week.")
    assert result["labels"] == []


def test_insufficient_context_is_flagged():
    detector = ManipulationDetector()
    result = detector.predict("This will destroy everything.")
    assert "insufficient_context" in result["labels"]
