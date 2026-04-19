# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_content_hash.py:7
# Component id: at.source.a1_at_functions.content_hash
from __future__ import annotations

__version__ = "0.1.0"

def content_hash(text: str) -> str:
    """SHA-256 (first 16 hex chars) of whitespace-normalised content."""
    normalised = "\n".join(line.rstrip() for line in text.splitlines()).strip()
    return hashlib.sha256(normalised.encode("utf-8")).hexdigest()[:16]
