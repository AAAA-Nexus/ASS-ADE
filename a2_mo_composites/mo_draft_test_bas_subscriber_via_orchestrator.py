# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testengineorchestrator.py:101
# Component id: mo.source.a2_mo_composites.test_bas_subscriber_via_orchestrator
from __future__ import annotations

__version__ = "0.1.0"

def test_bas_subscriber_via_orchestrator(self) -> None:
    o = EngineOrchestrator({})
    received: list = []
    o.bas.subscribe(lambda a: received.append(a.kind))
    o.on_step_start("task")
    o.on_step_end("response", {"trust_score": 0.05, "budget_pct": 0.99})
    assert len(received) >= 1
