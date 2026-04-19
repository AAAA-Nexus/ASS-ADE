# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testwisdomengine.py:42
# Component id: mo.source.ass_ade.test_conviction_ema
__version__ = "0.1.0"

    def test_conviction_ema(self) -> None:
        w = WisdomEngine({})
        r1 = w.run_audit({})  # score 0, conviction = 0.5*0.5 + 0.5*0 = 0.25
        assert abs(w.conviction - 0.25) < 0.01
        assert not w.is_confident  # well below 0.85
