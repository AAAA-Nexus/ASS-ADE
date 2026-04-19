# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testbas.py:64
# Component id: at.source.ass_ade.test_flush_alerts_drains_buffer
__version__ = "0.1.0"

    def test_flush_alerts_drains_buffer(self) -> None:
        b = BAS({})
        b.monitor_all({"synergy": 0.9, "trust_score": 0.1})
        flushed = b.flush_alerts()
        assert len(flushed) >= 1
        # second flush is empty
        assert b.flush_alerts() == []
