from src.models.predict import analyze_post


def test_analyze_post_returns_separate_dimensions():
    result = analyze_post("Share this now! Officials say sanctions will hit the region.")
    assert "engagement" in result
    assert "manipulation" in result
    assert "claims" in result
    assert "status" in result
