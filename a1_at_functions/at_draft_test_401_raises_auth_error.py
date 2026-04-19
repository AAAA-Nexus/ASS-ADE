# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testraiseforstatus.py:10
# Component id: at.source.ass_ade.test_401_raises_auth_error
__version__ = "0.1.0"

    def test_401_raises_auth_error(self) -> None:
        with pytest.raises(NexusAuthError) as exc_info:
            raise_for_status(401, endpoint="/v1/trust/score")
        assert exc_info.value.status_code == 401
