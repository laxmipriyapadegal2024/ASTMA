from __future__ import annotations

from typing import Any


def rank_evidence(claim: str, evidence_items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not claim or not evidence_items:
        return []

    ranked = []
    claim_lower = claim.lower()
    for item in evidence_items:
        snippet = str(item.get("snippet", "")).lower()
        relevance = 0.0
        if claim_lower in snippet or claim_lower in str(item.get("title", "")).lower():
            relevance += 0.6
        if any(term in snippet for term in ["official", "fact-check", "statement", "report", "announced"]):
            relevance += 0.2
        if str(item.get("support", "")).lower() == "support":
            relevance += 0.15
        if str(item.get("support", "")).lower() == "contradict":
            relevance += 0.1
        ranked.append({**item, "relevance": round(relevance, 2)})

    ranked.sort(key=lambda x: x.get("relevance", 0.0), reverse=True)
    return ranked
