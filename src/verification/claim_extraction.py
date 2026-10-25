from __future__ import annotations

import re
from typing import Any


def extract_claims(post_text: str) -> list[str]:
    if not post_text or not str(post_text).strip():
        return []

    text = str(post_text).strip()
    sentences = re.split(r"(?<=[.!?])\s+", text)
    claims: list[str] = []

    for sentence in sentences:
        if not sentence.strip():
            continue
        lower = sentence.lower()
        if any(phrase in lower for phrase in ["share this", "please share", "tag your friends", "comment below", "like and share", "repost this"]):
            continue
        if len(sentence.split()) < 4:
            continue
        if any(trigger in lower for trigger in ["officials", "government", "report", "said", "announced", "according", "stated", "trade", "sanctions", "election", "minister", "agency", "court"]):
            claims.append(sentence.strip())
    return claims


def evaluate_claim_evidence(claim: str, evidence: list[dict[str, Any]] | None) -> dict[str, Any]:
    if not claim or not str(claim).strip():
        return {"status": "not_a_verifiable_factual_claim", "explanation": "No claim was provided.", "evidence": []}

    if not evidence:
        return {"status": "unverified", "explanation": "No evidence was available for this claim.", "evidence": []}

    support_count = sum(1 for item in evidence if str(item.get("support", "")).lower() == "support")
    contradict_count = sum(1 for item in evidence if str(item.get("support", "")).lower() == "contradict")

    if support_count > 0 and contradict_count == 0:
        status = "supported_by_available_evidence"
        explanation = "The available evidence supports the claim."
    elif contradict_count > 0 and support_count == 0:
        status = "contradicted_by_available_evidence"
        explanation = "The available evidence contradicts the claim."
    elif support_count > 0 and contradict_count > 0:
        status = "mixed_or_context_dependent"
        explanation = "The available evidence is mixed and may require human review."
    else:
        status = "insufficient_evidence"
        explanation = "The available evidence is too weak or inconclusive to assess the claim."

    return {"status": status, "explanation": explanation, "evidence": evidence}
