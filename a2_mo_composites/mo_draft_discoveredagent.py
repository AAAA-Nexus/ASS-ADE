# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/models.py:334
# Component id: mo.source.ass_ade.discoveredagent
__version__ = "0.1.0"

class DiscoveredAgent(NexusModel):
    agent_id: Any = None
    name: str | None = None
    capabilities: Any = None
    reputation_score: float | None = None
    endpoint: str | None = None
    match_score: float | None = None
