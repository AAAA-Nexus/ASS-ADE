# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_engine_integration.py:199
# Component id: mo.source.ass_ade.test_capability_gap_alert
__version__ = "0.1.0"

    def test_capability_gap_alert(self) -> None:
        b = BAS({})
        alerts = b.monitor_all({"missing_capabilities": ["llm", "search"]})
        kinds = {a.kind for a in alerts}
        assert "capability_gap" in kinds
