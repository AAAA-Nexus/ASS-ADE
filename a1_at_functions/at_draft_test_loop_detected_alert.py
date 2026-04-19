# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testbas.py:44
# Component id: at.source.ass_ade.test_loop_detected_alert
__version__ = "0.1.0"

    def test_loop_detected_alert(self) -> None:
        b = BAS({})
        alerts = b.monitor_all({"tool_repeat_count": 5})
        kinds = {a.kind for a in alerts}
        assert "loop_detected" in kinds
