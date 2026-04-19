# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/agent/providers.py:350
# Component id: at.source.ass_ade.get_provider
__version__ = "0.1.0"

def get_provider(name: str) -> ProviderProfile | None:
    """Fetch a provider profile by name (case-insensitive)."""
    return FREE_PROVIDERS.get(name.lower())
