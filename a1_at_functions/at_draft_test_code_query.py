# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testlocalroute.py:12
# Component id: at.source.ass_ade.test_code_query
__version__ = "0.1.0"

    def test_code_query(self):
        decision = local_route("Write a function to parse JSON")
        assert decision.tier in (ModelTier.STANDARD, ModelTier.DEEP)
        assert decision.complexity >= 0.3
