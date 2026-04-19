# Extracted from C:/!ass-ade/tests/test_engine_integration.py:298
# Component id: mo.source.ass_ade.test_on_step_start_atlas_complexity
from __future__ import annotations

__version__ = "0.1.0"

def test_on_step_start_atlas_complexity(self) -> None:
    o = EngineOrchestrator({})
    result = o.on_step_start("a" * 2000)  # long = high complexity
    assert result["atlas_complexity"] > 1.0
