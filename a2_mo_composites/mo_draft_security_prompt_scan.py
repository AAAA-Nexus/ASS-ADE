# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:489
# Component id: mo.source.a2_mo_composites.security_prompt_scan
from __future__ import annotations

__version__ = "0.1.0"

def security_prompt_scan(self, prompt: str, **kwargs: Any) -> PromptScanResult:
    """/v1/security/prompt-scan — detect + block adversarial inputs. $0.040/request"""
    return self._post_model("/v1/security/prompt-scan", PromptScanResult, {"prompt": prompt, **kwargs})
