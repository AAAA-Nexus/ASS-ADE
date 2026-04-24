"""Tier a1 — assimilated function 'sig_fp'

Assimilated from: fingerprint.py:79-89
"""

from __future__ import annotations


# --- assimilated symbol ---
def sig_fp(source: str, language: Language | str) -> str:
    """Public dispatcher for signature fingerprint.

    Accepts any string for ``language`` to keep the public surface
    ergonomic; unsupported values raise
    :class:`UnsupportedLanguageError` eagerly.
    """

    if language == "python":
        return sig_fp_python(source)
    raise UnsupportedLanguageError(str(language))

