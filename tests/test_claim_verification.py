from src.verification.claim_extraction import extract_claims, evaluate_claim_evidence


def test_extract_claims_handles_no_claim():
    claims = extract_claims("Please share this with your friends!")
    assert claims == []


def test_evidence_status_for_relevant_supporting_evidence():
    result = evaluate_claim_evidence(
        "Officials announced a new trade restriction yesterday.",
        [
            {
                "title": "Trade restriction announced",
                "url": "https://example.com/1",
                "snippet": "Officials announced a new trade restriction yesterday.",
                "support": "support",
            }
        ],
    )
    assert result["status"] == "supported_by_available_evidence"


def test_evidence_status_for_no_evidence():
    result = evaluate_claim_evidence("A hidden government plan is underway.", [])
    assert result["status"] == "unverified"
