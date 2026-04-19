# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testbas.py:6
# Component id: at.source.ass_ade.test_monitor_synergy_alert
__version__ = "0.1.0"

    def test_monitor_synergy_alert(self) -> None:
        b = BAS({"synergy": {"threshold": 0.5}})
        a = b.monitor({"synergy": 0.8, "novelty": 0.0, "gvu_delta": 0.0})
        assert a is not None
        assert a.kind == "emergent_synergy"
        assert a.severity == "high"
