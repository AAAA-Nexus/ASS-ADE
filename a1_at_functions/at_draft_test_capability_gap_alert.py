# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testbas.py:32
# Component id: at.source.ass_ade.test_capability_gap_alert
__version__ = "0.1.0"

    def test_capability_gap_alert(self) -> None:
        b = BAS({})
        alerts = b.monitor_all({"missing_capabilities": ["llm", "search"]})
        kinds = {a.kind for a in alerts}
        assert "capability_gap" in kinds
