# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testwisdomengine.py:48
# Component id: mo.source.ass_ade.test_is_confident_true
__version__ = "0.1.0"

    def test_is_confident_true(self) -> None:
        w = WisdomEngine({"sde": {"conviction_required": 0.1}})
        # full state
        full = {f"q{i}": True for i in range(1, 51)}
        w.run_audit(full)
        assert w.is_confident
