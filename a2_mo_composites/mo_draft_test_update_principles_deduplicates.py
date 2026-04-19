# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_engine_integration.py:139
# Component id: mo.source.ass_ade.test_update_principles_deduplicates
__version__ = "0.1.0"

    def test_update_principles_deduplicates(self) -> None:
        w = WisdomEngine({})
        w.update_principles(["prefer reuse over regeneration"])
        w.update_principles(["prefer reuse over regeneration", "new principle"])
        assert w._principles.count("prefer reuse over regeneration") == 1
        assert "new principle" in w._principles
