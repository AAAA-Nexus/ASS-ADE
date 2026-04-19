# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testlseengine.py:28
# Component id: mo.source.ass_ade.test_high_trs_simple_task_gives_fast
__version__ = "0.1.0"

    def test_high_trs_simple_task_gives_fast(self):
        lse = self._make()
        decision = lse.select(trs_score=0.95, complexity="simple")
        assert decision.tier == "fast"
