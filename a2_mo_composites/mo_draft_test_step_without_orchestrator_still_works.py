# Extracted from C:/!ass-ade/tests/test_engine_integration.py:451
# Component id: mo.source.ass_ade.test_step_without_orchestrator_still_works
from __future__ import annotations

__version__ = "0.1.0"

def test_step_without_orchestrator_still_works(self) -> None:
    loop = self._make_loop(orchestrator=None)
    result = loop.step("Hello")
    assert isinstance(result, str)
