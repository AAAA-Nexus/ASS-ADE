"""Tier a1 — assimilated function 'slugify'

Assimilated from: rebuild/nexus_parse.py:95-99
"""

from __future__ import annotations


# --- assimilated symbol ---
def slugify(text: str) -> str:
    """CamelCase- and punctuation-aware slug: ``TokenBucket`` → ``token_bucket``."""
    spaced = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", text)
    out = re.sub(r"[^a-z0-9]+", "_", spaced.lower()).strip("_")
    return out or "component"

