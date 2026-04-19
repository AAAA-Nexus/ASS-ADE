# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_tier_prefix_from_id.py:7
# Component id: at.source.a1_at_functions.tier_prefix_from_id
from __future__ import annotations

__version__ = "0.1.0"

def tier_prefix_from_id(dep_id: str) -> str | None:
    """Return the two-letter tier prefix from a component id like ``at.parse.foo``."""
    if "." not in dep_id:
        return None
    prefix = dep_id.split(".", 1)[0]
    return prefix if prefix in _PREFIX_TO_TIER else None
