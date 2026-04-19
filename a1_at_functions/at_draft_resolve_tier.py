# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/agent/providers.py:380
# Component id: at.source.ass_ade.resolve_tier
__version__ = "0.1.0"

def resolve_tier(tier: str) -> str:
    """Normalize a tier name (e.g., 'haiku' → 'fast'). Returns canonical tier."""
    return TIER_ALIASES.get(tier.lower(), tier.lower())
