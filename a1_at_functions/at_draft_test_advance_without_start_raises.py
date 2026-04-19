# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testnexussession.py:19
# Component id: at.source.ass_ade.test_advance_without_start_raises
__version__ = "0.1.0"

    def test_advance_without_start_raises(self) -> None:
        session = NexusSession(_mock_client())
        with pytest.raises(RuntimeError, match="No active session"):
            session.advance()
