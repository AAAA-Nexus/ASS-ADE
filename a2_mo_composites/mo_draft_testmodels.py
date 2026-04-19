# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testmodels.py:7
# Component id: mo.source.a2_mo_composites.testmodels
from __future__ import annotations

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
