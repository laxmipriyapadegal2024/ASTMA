from __future__ import annotations

from src.models.engagement_classifier import EngagementDetector
from src.models.manipulation_classifier import ManipulationDetector
from src.verification.claim_extraction import evaluate_claim_evidence, extract_claims


def analyze_post(post_text: str, source_url: str = "", topic: str = "") -> dict:
    engagement = EngagementDetector().predict(post_text)
    manipulation = ManipulationDetector().predict(post_text)
    claims = extract_claims(post_text)

    claim_results = []
    for claim in claims:
        claim_results.append(
            {
                "text": claim,
                "status": evaluate_claim_evidence(claim, [])["status"],
                "evidence": [],
                "explanation": evaluate_claim_evidence(claim, [])["explanation"],
            }
        )

    return {
        "engagement": engagement,
        "manipulation": manipulation,
        "claims": claim_results,
        "status": "demo",
    }
