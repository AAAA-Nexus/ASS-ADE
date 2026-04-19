# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testloraflywheel.py:37
# Component id: at.source.ass_ade.test_capture_rejection_adds_negative
__version__ = "0.1.0"

    def test_capture_rejection_adds_negative(self, tmp_path):
        fly = self._make(tmp_path)
        fly.capture_rejection("bad code", "A03_injection_eval")
        assert fly._pending[0].kind == "rejection"
