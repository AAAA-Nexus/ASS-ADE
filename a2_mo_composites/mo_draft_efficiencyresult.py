# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_efficiencyresult.py:5
# Component id: mo.source.ass_ade.efficiencyresult
__version__ = "0.1.0"

class EfficiencyResult(NexusModel):
    """/v1/efficiency — PAY-506"""
    roi_signal: float | None = None
    interactions_analysed: int | None = None
    efficiency_score: float | None = None
