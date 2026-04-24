"""Tier a2 — assimilated class 'UnsupportedLanguageError'

Assimilated from: fingerprint.py:48-63
"""

from __future__ import annotations


# --- assimilated symbol ---
class UnsupportedLanguageError(FingerprintError):
    """Raised when fingerprinting is requested for a language whose
    implementation has not yet landed in this module.

    Not a stub: this is a real, shipped error path. The ``language``
    attribute carries the requested value; consumers use
    :data:`SUPPORTED_LANGUAGES` to enumerate what is available.
    """

    def __init__(self, language: str) -> None:
        self.language = language
        super().__init__(
            f"Fingerprinting for language {language!r} is not implemented "
            f"in this build. Supported languages: "
            f"{sorted(SUPPORTED_LANGUAGES)}."
        )

