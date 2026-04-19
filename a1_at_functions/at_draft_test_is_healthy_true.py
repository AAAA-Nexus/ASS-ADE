# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testnexussession.py:29
# Component id: at.source.ass_ade.test_is_healthy_true
__version__ = "0.1.0"

    def test_is_healthy_true(self) -> None:
        session = NexusSession(_mock_client())
        session.start("13608")
        assert session.is_healthy()
