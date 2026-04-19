# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testraiseforstatus.py:44
# Component id: at.source.ass_ade.test_custom_detail_message
__version__ = "0.1.0"

    def test_custom_detail_message(self) -> None:
        with pytest.raises(NexusServerError, match="oops"):
            raise_for_status(500, detail="oops")
