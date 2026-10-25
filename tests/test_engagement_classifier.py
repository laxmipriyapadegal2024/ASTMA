from src.models.engagement_classifier import EngagementDetector


def test_explicit_engagement_solicitation_detected():
    detector = EngagementDetector(model_path=None)
    result = detector.predict("Share this now! Like, comment, and tag your friends!")
    assert result["predicted_label"] == "engagement_bait"


def test_legitimate_public_service_call_not_bait():
    detector = EngagementDetector(model_path=None)
    result = detector.predict("Please share the official evacuation instructions with anyone who needs them.")
    assert result["predicted_label"] == "not_engagement_bait"


def test_untrained_model_reports_demo_status():
    detector = EngagementDetector(model_path=None)
    result = detector.predict("This is a test.")
    assert result["model_status"] == "demo_untrained"
