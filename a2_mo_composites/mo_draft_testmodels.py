# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_a2a.py:297
# Component id: mo.source.ass_ade.testmodels
__version__ = "0.1.0"

class TestModels:
    def test_agent_card_name_validation(self) -> None:
        with pytest.raises(Exception):
            A2AAgentCard(name="")

    def test_agent_card_with_payment(self) -> None:
        card = A2AAgentCard(name="Paid", payment={"type": "x402"})
        assert card.payment == {"type": "x402"}

    def test_validation_report_properties(self) -> None:
        issues = [
            ValidationIssue("error", "f1", "bad"),
            ValidationIssue("warning", "f2", "meh"),
            ValidationIssue("error", "f3", "also bad"),
        ]
        report = ValidationReport(valid=False, issues=issues)
        assert len(report.errors) == 2
        assert len(report.warnings) == 1
