# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testengineorchestrator.py:60
# Component id: mo.source.a2_mo_composites.test_on_step_end_gvu_updated
from __future__ import annotations

__version__ = "0.1.0"

def test_on_step_end_gvu_updated(self) -> None:
    o = EngineOrchestrator({})
    o.on_step_start("task")
    report = o.on_step_end("response", {})
    assert report.gvu_coefficient > 0.0
