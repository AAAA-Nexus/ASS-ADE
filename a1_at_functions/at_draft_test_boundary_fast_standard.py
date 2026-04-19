# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testtierforcomplexity.py:15
# Component id: at.source.ass_ade.test_boundary_fast_standard
__version__ = "0.1.0"

    def test_boundary_fast_standard(self):
        assert tier_for_complexity(0.29) == ModelTier.FAST
        assert tier_for_complexity(0.3) == ModelTier.STANDARD
