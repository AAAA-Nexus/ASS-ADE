# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testmodels.py:14
# Component id: at.source.ass_ade.test_validation_report_properties
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
