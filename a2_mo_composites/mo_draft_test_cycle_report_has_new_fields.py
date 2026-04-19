# Extracted from C:/!ass-ade/tests/test_phase_engines.py:691
# Component id: mo.source.ass_ade.test_cycle_report_has_new_fields
from __future__ import annotations

__version__ = "0.1.0"

def test_cycle_report_has_new_fields(self):
    from ass_ade.agent.orchestrator import CycleReport
    report = CycleReport(alerts=[])
    assert hasattr(report, "wisdom_ema")
    assert hasattr(report, "tca_stale_files")
    assert hasattr(report, "cie_passes")
    assert hasattr(report, "lora_pending")
    assert hasattr(report, "autopoietic_triggered")
