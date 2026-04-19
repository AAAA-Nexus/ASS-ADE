# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testnexuserrorhierarchy.py:14
# Component id: at.source.ass_ade.test_all_subclasses_inherit_from_base
__version__ = "0.1.0"

    def test_all_subclasses_inherit_from_base(self) -> None:
        for cls in (
            NexusConnectionError,
            NexusTimeoutError,
            NexusAuthError,
            NexusPaymentRequired,
            NexusRateLimited,
            NexusServerError,
            NexusValidationError,
            NexusCircuitOpen,
        ):
            assert issubclass(cls, NexusError)
            err = cls("test")
            assert isinstance(err, NexusError)
