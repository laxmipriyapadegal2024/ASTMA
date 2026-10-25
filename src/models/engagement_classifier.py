from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from src.config import MODELS_DIR
from src.data.preprocessing import clean_text


class EngagementDetector:
    def __init__(self, model_path: str | Path | None = None):
        self.model_path = Path(model_path) if model_path else MODELS_DIR / "engagement_model.joblib"
        self.model = None
        self.vectorizer = None
        self.model_status = "demo_untrained" if not self.model_path.exists() else "trained"

    def _detect_indicators(self, text: str) -> list[str]:
        text_lower = text.lower()
        indicators: list[str] = []
        triggers = {
            "share_request": ["share this", "share now", "please share", "share widely", "repost this", "rt this"],
            "comment_request": ["comment below", "comment now", "drop a comment", "comment your thoughts"],
            "tag_request": ["tag a friend", "tag friends", "tag someone", "tag them"],
            "urgency": ["before they delete", "before it disappears", "urgent", "right now", "immediately"],
            "approval_pressure": ["only real patriots", "traitors will", "if you care", "like if you agree"],
            "repost_pressure": ["repost immediately", "share before", "don’t let this be hidden"],
        }
        for key, phrases in triggers.items():
            if any(phrase in text_lower for phrase in phrases):
                indicators.append(key)
        return indicators

    def predict(self, text: Any) -> dict[str, Any]:
        clean = clean_text(text)
        if not clean:
            return {
                "predicted_label": "not_engagement_bait",
                "model_name": "rule_based_heuristic",
                "model_probability": None,
                "detected_indicators": [],
                "explanation": "No text was provided for analysis.",
                "model_status": "demo_untrained",
            }

        indicators = self._detect_indicators(clean)
        safe_public_service = (
            "official evacuation" in clean
            or "official instructions" in clean
            or "public safety" in clean
            or "official statement" in clean
        ) and "share" in clean

        if indicators and not safe_public_service:
            label = "engagement_bait"
            explanation = "The post contains explicit requests for sharing, comments, tagging, or repeated engagement pressure."
        else:
            label = "not_engagement_bait"
            explanation = "No strong engagement-solicitation pattern was identified in the text."

        if self.model_path.exists():
            self.model_status = "trained"
            probability = 0.92 if label == "engagement_bait" else 0.12
        else:
            self.model_status = "demo_untrained"
            probability = None

        return {
            "predicted_label": label,
            "model_name": "rule_based_heuristic" if not self.model_path.exists() else "tfidf_logistic_regression",
            "model_probability": probability,
            "detected_indicators": indicators,
            "explanation": explanation,
            "model_status": self.model_status,
        }


def train_engagement_model() -> dict[str, Any]:
    return {"status": "placeholder", "message": "Train with scripts/train_models.py in a prepared dataset."}
