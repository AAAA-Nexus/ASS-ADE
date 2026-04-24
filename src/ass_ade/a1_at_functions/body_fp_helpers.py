"""Tier a1 — assimilated function 'body_fp'

Assimilated from: fingerprint.py:92-100
"""

from __future__ import annotations


# --- assimilated symbol ---
def body_fp(source: str, language: Language | str) -> str:
    """Public dispatcher for body fingerprint.

    See :func:`sig_fp` for dispatch semantics.
    """

    if language == "python":
        return body_fp_python(source)
    raise UnsupportedLanguageError(str(language))

