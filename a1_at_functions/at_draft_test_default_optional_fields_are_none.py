# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testnexuserrorhierarchy.py:29
# Component id: at.source.ass_ade.test_default_optional_fields_are_none
__version__ = "0.1.0"

    def test_default_optional_fields_are_none(self) -> None:
        err = NexusError("minimal")
        assert err.status_code is None
        assert err.endpoint is None
        assert err.retry_after is None
