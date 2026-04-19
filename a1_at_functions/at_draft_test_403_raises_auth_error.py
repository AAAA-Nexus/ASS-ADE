# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testraiseforstatus.py:15
# Component id: at.source.ass_ade.test_403_raises_auth_error
__version__ = "0.1.0"

    def test_403_raises_auth_error(self) -> None:
        with pytest.raises(NexusAuthError):
            raise_for_status(403)
