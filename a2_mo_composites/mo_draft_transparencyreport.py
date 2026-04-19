# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_transparencyreport.py:5
# Component id: mo.source.ass_ade.transparencyreport
__version__ = "0.1.0"

class TransparencyReport(NexusModel):
    """/v1/compliance/transparency — TRP-100"""
    report_id: str | None = None
    period: str | None = None
    pdf_url: str | None = None
    machine_readable: dict | None = None
