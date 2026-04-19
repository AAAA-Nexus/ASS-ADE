# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testloraflywheel.py:135
# Component id: at.source.ass_ade.test_status_structure
__version__ = "0.1.0"

    def test_status_structure(self, tmp_path):
        fly = self._make(tmp_path)
        status = fly.status()
        assert hasattr(status, "adapter_version")
        assert hasattr(status, "contribution_count")
        assert hasattr(status, "ratchet_epoch")
        assert hasattr(status, "pending_count")
