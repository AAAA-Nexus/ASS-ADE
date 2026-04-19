# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_audit_report_has_warnings_field.py:7
# Component id: at.source.a1_at_functions.test_audit_report_has_warnings_field
from __future__ import annotations

__version__ = "0.1.0"

def test_audit_report_has_warnings_field(self) -> None:
    w = WisdomEngine({})
    report = w.run_audit({})
    assert hasattr(report, "warnings")
    assert isinstance(report.warnings, list)
