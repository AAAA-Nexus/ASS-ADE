# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testlocalroute.py:17
# Component id: at.source.ass_ade.test_decision_has_reason
__version__ = "0.1.0"

    def test_decision_has_reason(self):
        decision = local_route("Hello")
        assert "heuristic" in decision.reason.lower()
