# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testwisdomengine.py:112
# Component id: mo.source.ass_ade.test_report_returns_engine_info
__version__ = "0.1.0"

    def test_report_returns_engine_info(self) -> None:
        w = WisdomEngine({})
        r = w.report()
        assert r["engine"] == "wisdom"
        assert "conviction" in r and "conviction_required" in r
