# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testagentloopphase1.py:25
# Component id: at.source.ass_ade.test_d_max_increment_blocks_at_limit
__version__ = "0.1.0"

    def test_d_max_increment_blocks_at_limit(self):
        from ass_ade.agent.loop import D_MAX
        loop = self._make_loop()
        # Set depth to D_MAX so the next increment exceeds it
        loop._delegation_depth = D_MAX
        assert loop.increment_delegation_depth() is False
