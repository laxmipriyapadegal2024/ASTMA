import pandas as pd

from src.data.preprocessing import clean_text, duplicate_mask


def test_clean_text_handles_null_and_empty():
    assert clean_text(None) == ""
    assert clean_text("   ") == ""
    assert clean_text("Hello world") == "hello world"


def test_clean_text_preserves_negations_and_urls():
    text = "This is not a scam, and https://example.com is here #breaking"
    cleaned = clean_text(text)
    assert "not" in cleaned
    assert "https://example.com" in cleaned
    assert "#breaking" in cleaned


def test_duplicate_mask_detects_duplicates():
    df = pd.DataFrame({"text": ["A", "A", "B", "B"]})
    mask = duplicate_mask(df, "text")
    assert mask.tolist() == [False, True, False, True]
