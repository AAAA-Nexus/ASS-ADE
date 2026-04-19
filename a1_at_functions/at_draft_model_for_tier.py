# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_providerprofile.py:34
# Component id: at.source.ass_ade.model_for_tier
__version__ = "0.1.0"

    def model_for_tier(self, tier: str, override: dict[str, str] | None = None) -> str | None:
        """Get the model id for a tier, honoring config overrides."""
        tier = TIER_ALIASES.get(tier, tier)
        if override and tier in override:
            return override[tier]
        return self.models_by_tier.get(tier)
