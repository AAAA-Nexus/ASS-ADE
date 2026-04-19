# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_thinkroute.py:5
# Component id: mo.source.ass_ade.thinkroute
__version__ = "0.1.0"

class ThinkRoute(NexusModel):
    """/v1/routing/think — POP-1207"""
    complexity: Any = None   # "low" | "medium" | "high"
    recommended_tier: str | None = None
    recommended_model: str | None = None
