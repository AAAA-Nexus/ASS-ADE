# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/models.py:405
# Component id: mo.source.ass_ade.capabilitymatch
__version__ = "0.1.0"

class CapabilityMatch(NexusModel):
    """/v1/agents/capabilities/match"""
    matches: list[DiscoveredAgent] = Field(default_factory=list)
    task: str | None = None
