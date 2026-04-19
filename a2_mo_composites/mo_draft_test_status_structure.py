# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_phase_engines.py:537
# Component id: mo.source.ass_ade.test_status_structure
__version__ = "0.1.0"

    def test_status_structure(self, tmp_path):
        fly = self._make(tmp_path)
        status = fly.status()
        assert hasattr(status, "adapter_version")
        assert hasattr(status, "contribution_count")
        assert hasattr(status, "ratchet_epoch")
        assert hasattr(status, "pending_count")
