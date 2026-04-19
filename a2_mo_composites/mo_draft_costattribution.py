# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_costattribution.py:5
# Component id: mo.source.ass_ade.costattribution
__version__ = "0.1.0"

class CostAttribution(NexusModel):
    """/v1/costs/attribute — DEV-603"""
    total_tokens: int | None = None
    by_agent: dict | None = None
    by_task: dict | None = None
    by_model: dict | None = None
