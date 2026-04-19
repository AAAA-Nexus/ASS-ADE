# Extracted from C:/!ass-ade/src/ass_ade/nexus/client.py:672
# Component id: mo.source.ass_ade.prompt_inject_scan
from __future__ import annotations

__version__ = "0.1.0"

def prompt_inject_scan(self, prompt: str, **kwargs: Any) -> PromptScanResult:
    """/v1/prompts/inject-scan — adversarial injection detection. $0.040/request"""
    return self._post_model("/v1/prompts/inject-scan", PromptScanResult, {"prompt": prompt, **kwargs})
