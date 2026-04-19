# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testloraflywheel.py:31
# Component id: at.source.ass_ade.test_low_confidence_principle_skipped
__version__ = "0.1.0"

    def test_low_confidence_principle_skipped(self, tmp_path):
        fly = self._make(tmp_path)
        cid = fly.capture_principle("weak idea", confidence=0.1)
        assert cid == ""
        assert len(fly._pending) == 0
