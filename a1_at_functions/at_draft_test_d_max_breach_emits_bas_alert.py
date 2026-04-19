# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_d_max_breach_emits_bas_alert.py:7
# Component id: at.source.a1_at_functions.test_d_max_breach_emits_bas_alert
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
