# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a3_og_features/og_draft_safeexecuteresult.py:7
# Component id: og.source.a3_og_features.safeexecuteresult
from __future__ import annotations

__version__ = "0.1.0"

class SafeExecuteResult(BaseModel):
    tool_name: str | None = None
    shield_passed: bool = False
    prompt_scan_passed: bool = False
    invocation_result: dict[str, Any] = Field(default_factory=dict)
    certificate_id: str | None = None
