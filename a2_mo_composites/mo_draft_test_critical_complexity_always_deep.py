# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testlseengine.py:38
# Component id: mo.source.ass_ade.test_critical_complexity_always_deep
__version__ = "0.1.0"

    def test_critical_complexity_always_deep(self):
        lse = self._make()
        decision = lse.select(trs_score=0.9, complexity="critical")
        assert decision.tier == "deep"
