# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testloraflywheel.py:18
# Component id: at.source.ass_ade.test_capture_fix_adds_to_pending
__version__ = "0.1.0"

    def test_capture_fix_adds_to_pending(self, tmp_path):
        fly = self._make(tmp_path)
        cid = fly.capture_fix("old code", "new code")
        assert cid != ""
        assert len(fly._pending) == 1
        assert fly._pending[0].kind == "fix"
