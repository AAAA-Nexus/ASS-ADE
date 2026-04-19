# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_prompt_optimize.py:7
# Component id: at.source.a1_at_functions.prompt_optimize
from __future__ import annotations

__version__ = "0.1.0"

def prompt_optimize(self, prompt: str, **kwargs: Any) -> PromptOptimized:
    """/v1/prompts/optimize — rewrite for clarity, safety, lower cost. $0.040/request"""
    return self._post_model("/v1/prompts/optimize", PromptOptimized, {"prompt": prompt, **kwargs})
