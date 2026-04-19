# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_normal_flow_does_not_trigger_d_max_alert.py:7
# Component id: at.source.a1_at_functions.test_normal_flow_does_not_trigger_d_max_alert
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
