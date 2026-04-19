# Extracted from C:/!ass-ade/tests/test_phase1_integration.py:192
# Component id: at.source.ass_ade.test_normal_flow_does_not_trigger_d_max_alert
from __future__ import annotations

__version__ = "0.1.0"

def test_normal_flow_does_not_trigger_d_max_alert(self):
    provider = _make_provider_returning_text("ok")
    registry = ToolRegistry()
    orchestrator = EngineOrchestrator({})
    loop = AgentLoop(provider=provider, registry=registry, orchestrator=orchestrator)

    # Normal step (depth = 0)
    loop.step("normal request")
    alerts = orchestrator.bas._alerts
    kinds = [a.kind for a in alerts]
    assert "d_max_breach" not in kinds
