# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testnexussession.py:13
# Component id: at.source.ass_ade.test_advance_increments_epoch
__version__ = "0.1.0"

    def test_advance_increments_epoch(self) -> None:
        session = NexusSession(_mock_client())
        session.start("13608")
        session.advance()
        assert session.epoch == 1
