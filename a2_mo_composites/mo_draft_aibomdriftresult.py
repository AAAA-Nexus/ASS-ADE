# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/models.py:482
# Component id: mo.source.ass_ade.aibomdriftresult
__version__ = "0.1.0"

class AibomDriftResult(NexusModel):
    """/v1/aibom/drift"""
    drift_detected: bool | None = None
    lineage_hash: str | None = None
    verification_status: str | None = None
