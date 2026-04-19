# Extracted from C:/!ass-ade/src/ass_ade/protocol/cycle.py:13
# Component id: mo.source.ass_ade.protocolauditcheck
from __future__ import annotations

__version__ = "0.1.0"

class ProtocolAuditCheck(BaseModel):
    name: str
    passed: bool
    detail: str
