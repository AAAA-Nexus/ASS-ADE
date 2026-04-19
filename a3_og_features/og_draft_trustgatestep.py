# Extracted from C:/!ass-ade/src/ass_ade/workflows.py:32
# Component id: og.source.ass_ade.trustgatestep
from __future__ import annotations

__version__ = "0.1.0"

class TrustGateStep(BaseModel):
    name: str
    passed: bool
    detail: str = ""
    raw: dict[str, Any] = Field(default_factory=dict)
