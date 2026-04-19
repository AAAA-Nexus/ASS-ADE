# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_certifiedoutput.py:5
# Component id: mo.source.ass_ade.certifiedoutput
__version__ = "0.1.0"

class CertifiedOutput(NexusModel):
    """/v1/certify/output — OCN-100"""
    certificate_id: str | None = None
    score: float | None = None
    rubric_passed: bool | None = None
    valid_until: str | None = None
