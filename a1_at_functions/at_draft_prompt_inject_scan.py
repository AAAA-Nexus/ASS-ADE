# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_prompt_inject_scan.py:7
# Component id: at.source.a1_at_functions.prompt_inject_scan
from __future__ import annotations

__version__ = "0.1.0"

def prompt_inject_scan(self, prompt: str, **kwargs: Any) -> PromptScanResult:
    """/v1/prompts/inject-scan — adversarial injection detection. $0.040/request"""
    return self._post_model("/v1/prompts/inject-scan", PromptScanResult, {"prompt": prompt, **kwargs})
