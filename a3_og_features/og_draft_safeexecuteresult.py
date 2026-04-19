# Extracted from C:/!ass-ade/src/ass_ade/workflows.py:57
# Component id: og.source.ass_ade.safeexecuteresult
from __future__ import annotations

__version__ = "0.1.0"

class SafeExecuteResult(BaseModel):
    tool_name: str | None = None
    shield_passed: bool = False
    prompt_scan_passed: bool = False
    invocation_result: dict[str, Any] = Field(default_factory=dict)
    certificate_id: str | None = None
