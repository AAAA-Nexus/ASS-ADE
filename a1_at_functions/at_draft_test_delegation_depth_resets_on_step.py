# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testagentloopphase1.py:19
# Component id: at.source.ass_ade.test_delegation_depth_resets_on_step
__version__ = "0.1.0"

    def test_delegation_depth_resets_on_step(self):
        loop = self._make_loop()
        loop._delegation_depth = 10
        loop.reset_delegation_depth()
        assert loop.delegation_depth == 0
