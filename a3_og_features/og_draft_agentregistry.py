# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/models.py:350
# Component id: og.source.ass_ade.agentregistry
__version__ = "0.1.0"

class AgentRegistry(NexusModel):
    """/v1/discovery/registry"""
    agents: list[DiscoveredAgent] = Field(default_factory=list)
    total_registered: int | None = None
