# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:477
# Component id: mo.source.a2_mo_composites.prompt_inject_scan
from __future__ import annotations

__version__ = "0.1.0"

def prompt_inject_scan(self, prompt: str, **kwargs: Any) -> PromptScanResult:
    """/v1/prompts/inject-scan — adversarial injection detection. $0.040/request"""
    return self._post_model("/v1/prompts/inject-scan", PromptScanResult, {"prompt": prompt, **kwargs})
