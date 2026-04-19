# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testraiseforstatus.py:24
# Component id: at.source.ass_ade.test_422_raises_validation_error
__version__ = "0.1.0"

    def test_422_raises_validation_error(self) -> None:
        with pytest.raises(NexusValidationError):
            raise_for_status(422, detail="bad input")
