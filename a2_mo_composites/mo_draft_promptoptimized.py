# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:428
# Component id: mo.source.ass_ade.promptoptimized
from __future__ import annotations

__version__ = "0.1.0"

class PromptOptimized(NexusModel):
    """/v1/prompts/optimize"""
    original_tokens: int | None = None
    optimized_tokens: int | None = None
    optimized_prompt: str | None = None
    savings_pct: float | None = None
