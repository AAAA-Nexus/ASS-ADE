# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testengineorchestratorphase15.py:58
# Component id: mo.source.ass_ade.test_wisdom_ema_initialized
__version__ = "0.1.0"

    def test_wisdom_ema_initialized(self):
        orch = self._make()
        assert orch._wisdom_ema == 0.5
