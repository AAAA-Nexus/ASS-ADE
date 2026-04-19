# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testraiseforstatus.py:33
# Component id: sy.source.ass_ade.test_5xx_raises_server_error
__version__ = "0.1.0"

    def test_5xx_raises_server_error(self) -> None:
        for code in (500, 502, 503, 504):
            with pytest.raises(NexusServerError) as exc_info:
                raise_for_status(code)
            assert exc_info.value.status_code == code
