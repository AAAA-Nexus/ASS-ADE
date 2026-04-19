# Extracted from C:/!ass-ade/tests/test_errors.py:19
# Component id: mo.source.ass_ade.testnexuserrorhierarchy
from __future__ import annotations

__version__ = "0.1.0"

class TestNexusErrorHierarchy:
    def test_base_error_carries_context(self) -> None:
        err = NexusError("boom", status_code=500, endpoint="/health", retry_after=2.5)
        assert err.detail == "boom"
        assert err.status_code == 500
        assert err.endpoint == "/health"
        assert err.retry_after == 2.5
        assert str(err) == "boom"

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

    def test_default_optional_fields_are_none(self) -> None:
        err = NexusError("minimal")
        assert err.status_code is None
        assert err.endpoint is None
        assert err.retry_after is None
