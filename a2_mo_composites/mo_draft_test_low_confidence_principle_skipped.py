# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_phase_engines.py:433
# Component id: mo.source.ass_ade.test_low_confidence_principle_skipped
__version__ = "0.1.0"

    def test_low_confidence_principle_skipped(self, tmp_path):
        fly = self._make(tmp_path)
        cid = fly.capture_principle("weak idea", confidence=0.1)
        assert cid == ""
        assert len(fly._pending) == 0
