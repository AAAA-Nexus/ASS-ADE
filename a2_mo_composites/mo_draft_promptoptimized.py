# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/models.py:428
# Component id: mo.source.ass_ade.promptoptimized
__version__ = "0.1.0"

class PromptOptimized(NexusModel):
    """/v1/prompts/optimize"""
    original_tokens: int | None = None
    optimized_tokens: int | None = None
    optimized_prompt: str | None = None
    savings_pct: float | None = None
