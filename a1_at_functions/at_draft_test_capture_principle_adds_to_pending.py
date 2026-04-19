# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testloraflywheel.py:25
# Component id: at.source.ass_ade.test_capture_principle_adds_to_pending
__version__ = "0.1.0"

    def test_capture_principle_adds_to_pending(self, tmp_path):
        fly = self._make(tmp_path)
        cid = fly.capture_principle("always verify before acting", confidence=0.9)
        assert cid != ""
        assert fly._pending[0].kind == "principle"
