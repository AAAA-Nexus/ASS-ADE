# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_engine_integration.py:211
# Component id: mo.source.ass_ade.test_loop_detected_alert
__version__ = "0.1.0"

    def test_loop_detected_alert(self) -> None:
        b = BAS({})
        alerts = b.monitor_all({"tool_repeat_count": 5})
        kinds = {a.kind for a in alerts}
        assert "loop_detected" in kinds
