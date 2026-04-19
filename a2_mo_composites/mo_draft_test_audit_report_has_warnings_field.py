# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_engine_integration.py:146
# Component id: mo.source.ass_ade.test_audit_report_has_warnings_field
__version__ = "0.1.0"

    def test_audit_report_has_warnings_field(self) -> None:
        w = WisdomEngine({})
        report = w.run_audit({})
        assert hasattr(report, "warnings")
        assert isinstance(report.warnings, list)
