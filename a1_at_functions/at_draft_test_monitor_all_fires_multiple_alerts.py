# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testbas.py:18
# Component id: at.source.ass_ade.test_monitor_all_fires_multiple_alerts
__version__ = "0.1.0"

    def test_monitor_all_fires_multiple_alerts(self) -> None:
        b = BAS({})
        alerts = b.monitor_all({
            "synergy": 0.9,
            "novelty": 0.9,
            "trust_score": 0.1,
            "budget_pct": 0.95,
            "gvu_delta": 0.0,
        })
        kinds = {a.kind for a in alerts}
        assert "emergent_synergy" in kinds
        assert "trust_violation" in kinds
        assert "budget_exhaustion" in kinds
