# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_on_step_end_gvu_updated.py:7
# Component id: at.source.a1_at_functions.test_on_step_end_gvu_updated
from __future__ import annotations

__version__ = "0.1.0"

def test_on_step_end_gvu_updated(self) -> None:
    o = EngineOrchestrator({})
    o.on_step_start("task")
    report = o.on_step_end("response", {})
    assert report.gvu_coefficient > 0.0
