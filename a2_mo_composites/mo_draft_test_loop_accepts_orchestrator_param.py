# Extracted from C:/!ass-ade/tests/test_engine_integration.py:435
# Component id: mo.source.ass_ade.test_loop_accepts_orchestrator_param
from __future__ import annotations

__version__ = "0.1.0"

def test_loop_accepts_orchestrator_param(self) -> None:
    o = EngineOrchestrator({})
    loop = self._make_loop(orchestrator=o)
    assert loop._orchestrator is o
