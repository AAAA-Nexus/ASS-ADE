# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testagentlooporchestrator.py:41
# Component id: sy.source.a2_mo_composites.test_step_without_orchestrator_still_works
from __future__ import annotations

__version__ = "0.1.0"

def test_step_without_orchestrator_still_works(self) -> None:
    loop = self._make_loop(orchestrator=None)
    result = loop.step("Hello")
    assert isinstance(result, str)
