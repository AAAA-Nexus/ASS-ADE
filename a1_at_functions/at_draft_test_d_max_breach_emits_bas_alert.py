# Extracted from C:/!ass-ade/tests/test_phase1_integration.py:173
# Component id: at.source.ass_ade.test_d_max_breach_emits_bas_alert
from __future__ import annotations

__version__ = "0.1.0"

def test_d_max_breach_emits_bas_alert(self):
    provider = _make_provider_returning_text("ok")
    registry = ToolRegistry()
    orchestrator = EngineOrchestrator({})
    loop = AgentLoop(provider=provider, registry=registry, orchestrator=orchestrator)

    # Set to exactly D_MAX so next increment exceeds
    loop._delegation_depth = D_MAX
    loop.step("[REFINE round 1/3] retry")

    # BAS should have a d_max_breach alert
    alerts = orchestrator.bas._alerts
    kinds = [a.kind for a in alerts]
    assert "d_max_breach" in kinds, f"Expected d_max_breach in {kinds}"
