from __future__ import annotations

from urllib.parse import urlparse


def validate_source_url(url: str) -> bool:
    if not url or not isinstance(url, str):
        return False
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        return False
    if parsed.hostname in {"localhost", "127.0.0.1"}:
        return False
    return True
