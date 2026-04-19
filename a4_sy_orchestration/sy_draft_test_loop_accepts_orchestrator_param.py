# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testagentlooporchestrator.py:25
# Component id: sy.source.a2_mo_composites.test_loop_accepts_orchestrator_param
from __future__ import annotations

__version__ = "0.1.0"

def test_loop_accepts_orchestrator_param(self) -> None:
    o = EngineOrchestrator({})
    loop = self._make_loop(orchestrator=o)
    assert loop._orchestrator is o
