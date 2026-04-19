# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testlseengine.py:55
# Component id: mo.source.ass_ade.test_fail_open_on_internal_error
__version__ = "0.1.0"

    def test_fail_open_on_internal_error(self):
        lse = self._make({"lse": {"default_tier": "balanced"}})
        # Corrupt internal state — should still return a decision
        lse._trs_haiku_threshold = "not_a_float"  # type: ignore
        decision = lse.select(trs_score=0.9)
        assert decision.model is not None
