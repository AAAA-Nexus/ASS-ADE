# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_on_step_start_atlas_complexity.py:7
# Component id: at.source.a1_at_functions.test_on_step_start_atlas_complexity
from __future__ import annotations

__version__ = "0.1.0"

def test_on_step_start_atlas_complexity(self) -> None:
    o = EngineOrchestrator({})
    result = o.on_step_start("a" * 2000)  # long = high complexity
    assert result["atlas_complexity"] > 1.0
