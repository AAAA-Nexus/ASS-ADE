# Extracted from C:/!ass-ade/src/ass_ade/nexus/client.py:587
# Component id: mo.source.ass_ade.sla_register
from __future__ import annotations

__version__ = "0.1.0"

def sla_register(self, agent_id: str, latency_ms: float, uptime_pct: float, error_rate: float, bond_usdc: float, **kwargs: Any) -> SlaRegistration:
    """/v1/sla/register — commit to SLA with bond. $0.080/call"""
    return self._post_model("/v1/sla/register", SlaRegistration, {
        "agent_id": agent_id, "latency_ms": latency_ms, "uptime_pct": uptime_pct,
        "error_rate": error_rate, "bond_usdc": bond_usdc, **kwargs,
    })
