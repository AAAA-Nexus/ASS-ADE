# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_consensussession.py:5
# Component id: mo.source.ass_ade.consensussession
__version__ = "0.1.0"

class ConsensusSession(NexusModel):
    """/v1/consensus/session — CSN-100"""
    session_id: str | None = None
    quorum_mode: str | None = None
    required_votes: int | None = None
    status: str | None = None
