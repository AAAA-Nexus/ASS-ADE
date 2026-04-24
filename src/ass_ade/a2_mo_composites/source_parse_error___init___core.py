"""Tier a2 — assimilated method 'SourceParseError.__init__'

Assimilated from: fingerprint.py:69-72
"""

from __future__ import annotations


# --- assimilated symbol ---
def __init__(self, language: str, detail: str) -> None:
    self.language = language
    self.detail = detail
    super().__init__(f"Could not parse {language} source: {detail}")

