# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/agent/providers.py:345
# Component id: at.source.ass_ade.list_providers
__version__ = "0.1.0"

def list_providers() -> list[str]:
    """All provider names known to the catalog."""
    return list(FREE_PROVIDERS.keys())
