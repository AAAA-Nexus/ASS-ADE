# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_portabilitycheck.py:5
# Component id: mo.source.ass_ade.portabilitycheck
__version__ = "0.1.0"

class PortabilityCheck(NexusModel):
    """/v1/federation/portability — AIF-102"""
    portability_score: float | None = None
    from_platform: str | None = None
    to_platform: str | None = None
    capability_gaps: list[str] = Field(default_factory=list)
