"""Tier a2 — assimilated method 'UnsupportedLanguageError.__init__'

Assimilated from: fingerprint.py:57-63
"""

from __future__ import annotations


# --- assimilated symbol ---
def __init__(self, language: str) -> None:
    self.language = language
    super().__init__(
        f"Fingerprinting for language {language!r} is not implemented "
        f"in this build. Supported languages: "
        f"{sorted(SUPPORTED_LANGUAGES)}."
    )

