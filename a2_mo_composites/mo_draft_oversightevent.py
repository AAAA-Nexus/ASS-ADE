# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_oversightevent.py:5
# Component id: mo.source.ass_ade.oversightevent
__version__ = "0.1.0"

class OversightEvent(NexusModel):
    """/v1/compliance/oversight — OVS-100"""
    event_id: str | None = None
    attestation: str | None = None
    reviewer: str | None = None
    timestamp: str | None = None
