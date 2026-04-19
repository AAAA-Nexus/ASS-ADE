# Extracted from C:/!ass-ade/tests/test_a2a.py:306
# Component id: at.source.ass_ade.test_validation_report_properties
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
