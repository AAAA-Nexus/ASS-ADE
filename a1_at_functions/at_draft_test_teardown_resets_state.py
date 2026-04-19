# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testnexussession.py:41
# Component id: at.source.ass_ade.test_teardown_resets_state
__version__ = "0.1.0"

    def test_teardown_resets_state(self) -> None:
        session = NexusSession(_mock_client())
        session.start("13608")
        session.teardown()
        assert not session.is_active
        assert session.session_id is None
        assert session.epoch == 0
