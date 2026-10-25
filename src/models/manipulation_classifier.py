from __future__ import annotations

from typing import Any

from src.data.preprocessing import clean_text


class ManipulationDetector:
    def __init__(self):
        self.model_status = "rule_based_heuristic"

    def predict(self, text: Any) -> dict[str, Any]:
        clean = clean_text(text)
        if not clean:
            return {"labels": [], "indicators": [], "summary": "No text to classify.", "status": "rule_based_heuristic"}

        labels: list[str] = []
        indicators: list[str] = []

        urgency_phrases = ["share now", "before they hide", "urgent", "immediately", "right now"]
        if any(phrase in clean for phrase in urgency_phrases):
            labels.append("urgency_pressure")
            indicators.append("urgency")

        if any(term in clean for term in ["everyone must", "must act now", "do not ignore", "tell everyone", "share now", "share this", "tag friends", "tag a friend", "repost this"]):
            labels.append("social_pressure")
            indicators.append("social pressure")

        if any(term in clean for term in ["elite", "cabal", "secret plan", "they are plotting", "global conspiracy"]):
            labels.append("unsupported_conspiracy_framing")
            indicators.append("conspiracy framing")

        if any(term in clean for term in ["either", "or else", "choose one", "join us or"]):
            labels.append("false_dilemma")
            indicators.append("false dilemma")

        if any(term in clean for term in ["traitors", "cowards", "enemy", "they are against us"]):
            labels.append("identity_based_pressure")
            indicators.append("identity pressure")

        if any(term in clean for term in ["destroy", "collapse", "disaster", "devastating", "panic"]):
            labels.append("fear_appeal")
            indicators.append("fear appeal")

        if any(term in clean for term in ["shocking", "outrageous", "disgusting", "appalling", "furious"]):
            labels.append("outrage_appeal")
            indicators.append("outrage appeal")

        if any(term in clean for term in ["this will destroy everything", "this is the end", "nothing else matters"]):
            labels.append("insufficient_context")

        if not labels and len(clean.split()) < 8 and any(term in clean for term in ["destroy", "everything", "immediately", "secret"]):
            labels.append("insufficient_context")
            indicators.append("weak evidence context")

        if not labels and any(term in clean for term in ["official", "said", "according to", "reported"]):
            labels = []
            indicators = []

        summary = (
            "Possible manipulation indicators were identified."
            if labels
            else "No clear manipulation indicators were found in the text."
        )
        return {
            "labels": labels,
            "indicators": indicators,
            "summary": summary,
            "status": self.model_status,
        }
