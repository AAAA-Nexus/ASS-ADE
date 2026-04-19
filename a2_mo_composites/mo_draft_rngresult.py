# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/models.py:192
# Component id: mo.source.ass_ade.rngresult
__version__ = "0.1.0"

class RngResult(NexusModel):
    """/v1/rng/quantum"""
    numbers: list[float] = Field(default_factory=list)
    seed_ts: str | None = None
    proof: str | None = None
    verified: bool | None = None
