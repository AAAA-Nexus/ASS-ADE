# Extracted from C:/!ass-ade/tests/test_errors.py:28
# Component id: at.source.ass_ade.test_all_subclasses_inherit_from_base
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
