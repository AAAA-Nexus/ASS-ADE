# Extracted from C:/!ass-ade/src/ass_ade/nexus/client.py:676
# Component id: mo.source.ass_ade.prompt_optimize
from __future__ import annotations

__version__ = "0.1.0"

def prompt_optimize(self, prompt: str, **kwargs: Any) -> PromptOptimized:
    """/v1/prompts/optimize — rewrite for clarity, safety, lower cost. $0.040/request"""
    return self._post_model("/v1/prompts/optimize", PromptOptimized, {"prompt": prompt, **kwargs})
