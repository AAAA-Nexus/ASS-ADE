# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testbas.py:100
# Component id: at.source.ass_ade.test_report_structure
__version__ = "0.1.0"

    def test_report_structure(self) -> None:
        b = BAS({})
        r = b.report()
        assert r["engine"] == "bas"
        assert "alerts_total" in r
        assert "alerts_session" in r
        assert "unflushed" in r
        assert "cooldown_s" in r
