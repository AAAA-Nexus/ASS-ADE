# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_validation_report_properties.py:7
# Component id: at.source.a1_at_functions.test_validation_report_properties
from __future__ import annotations

__version__ = "0.1.0"

def test_validation_report_properties(self) -> None:
    issues = [
        ValidationIssue("error", "f1", "bad"),
        ValidationIssue("warning", "f2", "meh"),
        ValidationIssue("error", "f3", "also bad"),
    ]
    report = ValidationReport(valid=False, issues=issues)
    assert len(report.errors) == 2
    assert len(report.warnings) == 1
