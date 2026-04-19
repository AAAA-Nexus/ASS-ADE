# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_resolve_tier.py:7
# Component id: at.source.a1_at_functions.resolve_tier
from __future__ import annotations

__version__ = "0.1.0"

def resolve_tier(tier: str) -> str:
    """Normalize a tier name (e.g., 'haiku' → 'fast'). Returns canonical tier."""
    return TIER_ALIASES.get(tier.lower(), tier.lower())
