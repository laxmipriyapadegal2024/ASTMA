from __future__ import annotations

from typing import Any


class ClaimClassifier:
    def __init__(self):
        self.model_status = "demo_untrained"

    def predict(self, claim: Any) -> dict[str, Any]:
        return {
            "predicted_verdict": "unverified",
            "model_status": self.model_status,
            "explanation": "This placeholder claim classifier is a transparent demo only.",
        }
