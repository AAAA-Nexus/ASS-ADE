# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_explaincert.py:5
# Component id: mo.source.ass_ade.explaincert
__version__ = "0.1.0"

class ExplainCert(NexusModel):
    """/v1/compliance/explain — XPL-100"""
    certificate_id: str | None = None
    feature_attribution: dict | None = None
    gdpr_art22_ready: bool | None = None
