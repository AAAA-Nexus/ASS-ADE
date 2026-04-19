# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testbas.py:92
# Component id: at.source.ass_ade.test_alert_severity_mapping
__version__ = "0.1.0"

    def test_alert_severity_mapping(self) -> None:
        b = BAS({})
        high_kinds = ["emergent_synergy", "gvu_jump", "trust_violation", "budget_exhaustion"]
        for kind in high_kinds:
            a = Alert(kind=kind, severity="", payload={}, ts="")
            b_alert = b.alert(kind, {})
            assert b_alert.severity == "high", f"{kind} should be high severity"
