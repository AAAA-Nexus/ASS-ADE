# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_model_for_tier.py:7
# Component id: at.source.a1_at_functions.model_for_tier
from __future__ import annotations

__version__ = "0.1.0"

def model_for_tier(self, tier: str, override: dict[str, str] | None = None) -> str | None:
    """Get the model id for a tier, honoring config overrides."""
    tier = TIER_ALIASES.get(tier, tier)
    if override and tier in override:
        return override[tier]
    return self.models_by_tier.get(tier)
