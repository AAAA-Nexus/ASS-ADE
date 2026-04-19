# Extracted from C:/!ass-ade/tests/test_errors.py:50
# Component id: mo.source.ass_ade.testraiseforstatus
from __future__ import annotations

__version__ = "0.1.0"

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
