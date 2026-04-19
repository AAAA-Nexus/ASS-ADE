# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_promptoptimized.py:7
# Component id: mo.source.a2_mo_composites.promptoptimized
from __future__ import annotations

__version__ = "0.1.0"

class PromptOptimized(NexusModel):
    """/v1/prompts/optimize"""
    original_tokens: int | None = None
    optimized_tokens: int | None = None
    optimized_prompt: str | None = None
    savings_pct: float | None = None
