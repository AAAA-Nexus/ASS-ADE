# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testraiseforstatus.py:39
# Component id: at.source.ass_ade.test_unknown_4xx_raises_base_error
__version__ = "0.1.0"

    def test_unknown_4xx_raises_base_error(self) -> None:
        with pytest.raises(NexusError) as exc_info:
            raise_for_status(418)
        assert exc_info.value.status_code == 418
