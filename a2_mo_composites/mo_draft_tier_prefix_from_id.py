# Extracted from C:/!ass-ade/src/ass_ade/engine/rebuild/tier_purity.py:33
# Component id: mo.source.ass_ade.tier_prefix_from_id
from __future__ import annotations

__version__ = "0.1.0"

def tier_prefix_from_id(dep_id: str) -> str | None:
    """Return the two-letter tier prefix from a component id like ``at.parse.foo``."""
    if "." not in dep_id:
        return None
    prefix = dep_id.split(".", 1)[0]
    return prefix if prefix in _PREFIX_TO_TIER else None
