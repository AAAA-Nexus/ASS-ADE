# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/models.py:145
# Component id: mo.source.ass_ade.entropyresult
__version__ = "0.1.0"

class EntropyResult(NexusModel):
    """/v1/oracle/entropy"""
    entropy_bits: float | None = None
    epoch: int | None = None
    verdict: str | None = None
