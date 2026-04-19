# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_all_subclasses_inherit_from_base.py:7
# Component id: at.source.a1_at_functions.test_all_subclasses_inherit_from_base
from __future__ import annotations

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
