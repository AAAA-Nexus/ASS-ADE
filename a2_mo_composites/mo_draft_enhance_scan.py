# Extracted from C:/!ass-ade/src/ass_ade/nexus/client.py:1462
# Component id: mo.source.ass_ade.enhance_scan
from __future__ import annotations

__version__ = "0.1.0"

def enhance_scan(
    self,
    local_report: dict[str, Any],
    agent_id: str | None = None,
) -> EnhanceScanResult:
    """Deep enhancement scan and blueprint generation via AAAA-Nexus."""
    payload: dict[str, Any] = {"local_report": local_report}
    if agent_id:
        payload["agent_id"] = agent_id
    return self._post_model("/v1/enhance/scan", EnhanceScanResult, payload)
