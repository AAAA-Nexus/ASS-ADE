# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a0_qk_constants/qk_draft_lineageproof.py:5
# Component id: qk.source.ass_ade.lineageproof
__version__ = "0.1.0"

class LineageProof(NexusModel):
    """/v1/compliance/lineage — LIN-100"""
    chain_hash: str | None = None
    stages: int | None = None
    integrity_ok: bool | None = None
