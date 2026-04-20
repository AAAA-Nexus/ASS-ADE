"""Tests for the typed exception hierarchy and status-code mapping."""

import pytest

from ass_ade.nexus.errors import (
    NexusAuthError,
    NexusCircuitOpen,
    NexusConnectionError,
    NexusError,
    NexusPaymentRequired,
    NexusRateLimited,
    NexusServerError,
    NexusTimeoutError,
    NexusValidationError,
    raise_for_status,
)


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


class TestRaiseForStatus:
    def test_2xx_does_nothing(self) -> None:
        for code in (200, 201, 204, 299):
            raise_for_status(code)  # should not raise

    def test_401_raises_auth_error(self) -> None:
        with pytest.raises(NexusAuthError) as exc_info:
            raise_for_status(401, endpoint="/v1/trust/score")
        assert exc_info.value.status_code == 401

    def test_403_raises_auth_error(self) -> None:
        with pytest.raises(NexusAuthError):
            raise_for_status(403)

    def test_402_raises_payment_required(self) -> None:
        with pytest.raises(NexusPaymentRequired) as exc_info:
            raise_for_status(402, endpoint="/v1/inference")
        assert exc_info.value.status_code == 402

    def test_422_raises_validation_error(self) -> None:
        with pytest.raises(NexusValidationError):
            raise_for_status(422, detail="bad input")

    def test_429_raises_rate_limited_with_retry_after(self) -> None:
        with pytest.raises(NexusRateLimited) as exc_info:
            raise_for_status(429, retry_after=5.0)
        assert exc_info.value.retry_after == 5.0

    def test_5xx_raises_server_error(self) -> None:
        for code in (500, 502, 503, 504):
            with pytest.raises(NexusServerError) as exc_info:
                raise_for_status(code)
            assert exc_info.value.status_code == code

    def test_unknown_4xx_raises_base_error(self) -> None:
        with pytest.raises(NexusError) as exc_info:
            raise_for_status(418)
        assert exc_info.value.status_code == 418

    def test_custom_detail_message(self) -> None:
        with pytest.raises(NexusServerError, match="oops"):
            raise_for_status(500, detail="oops")
