"""Tier a1 — assimilated function 'content_hash'

Assimilated from: rebuild/version_tracker.py:65-68
"""

from __future__ import annotations


# --- assimilated symbol ---
def content_hash(text: str) -> str:
    """SHA-256 (first 16 hex chars) of whitespace-normalised content."""
    normalised = "\n".join(line.rstrip() for line in text.splitlines()).strip()
    return hashlib.sha256(normalised.encode("utf-8")).hexdigest()[:16]

