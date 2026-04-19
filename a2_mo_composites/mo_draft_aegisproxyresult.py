# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:513
# Component id: mo.source.ass_ade.aegisproxyresult
from __future__ import annotations

__version__ = "0.1.0"

class AegisProxyResult(NexusModel):
    """/v1/aegis/mcp-proxy/execute"""
    allowed: bool | None = None
    tool_result: dict | None = None
    entropy_bound: float | None = None
    firewall_verdict: str | None = None
