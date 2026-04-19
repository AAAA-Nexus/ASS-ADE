# Extracted from C:/!ass-ade/src/ass_ade/engine/rebuild/version_tracker.py:65
# Component id: mo.source.ass_ade.content_hash
from __future__ import annotations

__version__ = "0.1.0"

def content_hash(text: str) -> str:
    """SHA-256 (first 16 hex chars) of whitespace-normalised content."""
    normalised = "\n".join(line.rstrip() for line in text.splitlines()).strip()
    return hashlib.sha256(normalised.encode("utf-8")).hexdigest()[:16]
