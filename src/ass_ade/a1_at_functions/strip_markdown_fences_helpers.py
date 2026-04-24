"""Tier a1 — assimilated function 'strip_markdown_fences'

Assimilated from: rebuild/nexus_parse.py:19-26
"""

from __future__ import annotations


# --- assimilated symbol ---
def strip_markdown_fences(text: str) -> str:
    """Strip a single surrounding ```lang fenced block if present."""
    if not isinstance(text, str):
        return ""
    m = _FENCE_RE.match(text.strip())
    if m:
        return m.group("body")
    return text

