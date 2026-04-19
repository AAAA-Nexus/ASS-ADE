# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_test_engine_report_aggregates_initialized_engines.py:7
# Component id: mo.source.a2_mo_composites.test_engine_report_aggregates_initialized_engines
from __future__ import annotations

__version__ = "0.1.0"

def test_engine_report_aggregates_initialized_engines(self) -> None:
    o = EngineOrchestrator({})
    _ = o.atlas  # initialize atlas
    _ = o.bas    # initialize bas
    reports = o.engine_report()
    assert "atlas" in reports
    assert "bas" in reports
