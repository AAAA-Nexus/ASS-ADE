# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:444
# Component id: mo.source.ass_ade.zerodayresult
from __future__ import annotations

__version__ = "0.1.0"

class ZeroDayResult(NexusModel):
    """/v1/security/zero-day"""
    vulnerable: bool | None = None
    patterns_matched: list[str] = Field(default_factory=list)
    severity: str | None = None
