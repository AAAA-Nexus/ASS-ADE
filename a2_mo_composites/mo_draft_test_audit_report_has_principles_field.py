# Extracted from C:/!ass-ade/tests/test_engine_integration.py:152
# Component id: mo.source.ass_ade.test_audit_report_has_principles_field
from __future__ import annotations

__version__ = "0.1.0"

def test_audit_report_has_principles_field(self) -> None:
    w = WisdomEngine({})
    report = w.run_audit({})
    assert hasattr(report, "principles")
    assert isinstance(report.principles, list)
