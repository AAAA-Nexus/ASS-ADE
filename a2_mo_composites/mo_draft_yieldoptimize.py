# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_yieldoptimize.py:5
# Component id: mo.source.ass_ade.yieldoptimize
__version__ = "0.1.0"

class YieldOptimize(NexusModel):
    """/v1/defi/yield-optimize — YLD-100"""
    allocations: list[dict] = Field(default_factory=list)
    expected_apy: float | None = None
    alpha_above_baseline: float | None = None
