# Extracted from C:/!ass-ade/src/ass_ade/agent/providers.py:73
# Component id: at.source.ass_ade.model_for_tier
from __future__ import annotations

__version__ = "0.1.0"

def model_for_tier(self, tier: str, override: dict[str, str] | None = None) -> str | None:
    """Get the model id for a tier, honoring config overrides."""
    tier = TIER_ALIASES.get(tier, tier)
    if override and tier in override:
        return override[tier]
    return self.models_by_tier.get(tier)
