# Extracted from C:/!ass-ade/tests/test_engine_integration.py:337
# Component id: mo.source.ass_ade.test_on_step_end_gvu_updated
from __future__ import annotations

__version__ = "0.1.0"

def test_on_step_end_gvu_updated(self) -> None:
    o = EngineOrchestrator({})
    o.on_step_start("task")
    report = o.on_step_end("response", {})
    assert report.gvu_coefficient > 0.0
