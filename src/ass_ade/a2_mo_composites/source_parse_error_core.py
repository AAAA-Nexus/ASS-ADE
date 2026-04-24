"""Tier a2 — assimilated class 'SourceParseError'

Assimilated from: fingerprint.py:66-72
"""

from __future__ import annotations


# --- assimilated symbol ---
class SourceParseError(FingerprintError):
    """Raised when the source cannot be parsed."""

    def __init__(self, language: str, detail: str) -> None:
        self.language = language
        self.detail = detail
        super().__init__(f"Could not parse {language} source: {detail}")

