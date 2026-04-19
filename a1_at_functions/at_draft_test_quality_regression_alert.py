# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testbas.py:38
# Component id: at.source.ass_ade.test_quality_regression_alert
__version__ = "0.1.0"

    def test_quality_regression_alert(self) -> None:
        b = BAS({})
        alerts = b.monitor_all({"score_delta": -0.5})
        kinds = {a.kind for a in alerts}
        assert "quality_regression" in kinds
