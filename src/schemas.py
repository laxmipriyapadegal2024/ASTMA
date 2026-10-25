from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class EvidenceItem:
    title: str = ""
    url: str = ""
    snippet: str = ""
    source_type: str = "unavailable"
    publication_date: str | None = None
    support: str = "unknown"
    relevance: float = 0.0
    notes: str = ""


@dataclass
class ClaimResult:
    text: str
    status: str = "unverified"
    evidence: list[EvidenceItem] = field(default_factory=list)
    explanation: str = ""


@dataclass
class AnalysisResult:
    engagement: dict[str, Any]
    manipulation: dict[str, Any]
    claims: list[ClaimResult]
    status: str = "demo"
