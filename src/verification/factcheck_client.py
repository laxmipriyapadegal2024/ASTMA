from __future__ import annotations

import os
from typing import Any

import requests


class FactCheckClient:
    def __init__(self, api_key: str | None = None, api_url: str | None = None):
        self.api_key = api_key or os.getenv("FACTCHECK_API_KEY")
        self.api_url = api_url or os.getenv("FACTCHECK_API_URL")

    def query(self, claim: str) -> list[dict[str, Any]]:
        if not self.api_key or not self.api_url:
            return []
        try:
            response = requests.get(
                self.api_url,
                params={"query": claim},
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=10,
            )
            response.raise_for_status()
            payload = response.json()
            if isinstance(payload, dict) and "claims" in payload:
                return payload["claims"]
            if isinstance(payload, list):
                return payload
        except requests.RequestException:
            return []
        return []
