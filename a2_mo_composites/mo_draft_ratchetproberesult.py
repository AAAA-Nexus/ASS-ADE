# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/models.py:177
# Component id: mo.source.ass_ade.ratchetproberesult
__version__ = "0.1.0"

class RatchetProbeResult(NexusModel):
    """/v1/ratchet/probe — batch health check"""
    results: list[dict] = Field(default_factory=list)
