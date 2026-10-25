from src.features.ngrams import extract_top_ngrams


def test_extract_top_ngrams_returns_most_common_phrases():
    texts = ["share now share now", "share now please", "officials met today"]
    top = extract_top_ngrams(texts, n=2, top_k=5)
    assert any(item[0] == "share now" for item in top)
    assert top[0][1] >= 2
