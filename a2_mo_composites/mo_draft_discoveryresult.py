# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/models.py:343
# Component id: mo.source.ass_ade.discoveryresult
__version__ = "0.1.0"

class DiscoveryResult(NexusModel):
    """/v1/discovery/search and /v1/discovery/recommend"""
    agents: list[DiscoveredAgent] = Field(default_factory=list)
    total: int | None = None
    query: Any = None
