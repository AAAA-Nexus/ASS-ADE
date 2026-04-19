# Extracted from C:/!ass-ade/tests/test_resilience.py:46
# Component id: mo.source.ass_ade.testretrytransport
from __future__ import annotations

__version__ = "0.1.0"

class TestRetryTransport:
    def test_success_on_first_try(self) -> None:
        inner = _CountingTransport([httpx.Response(200)])
        transport = RetryTransport(inner, max_retries=3, backoff_base=0.0)
        response = transport.handle_request(httpx.Request("GET", "https://example.com"))
        assert response.status_code == 200
        assert inner.call_count == 1

    def test_retries_on_500_then_succeeds(self) -> None:
        inner = _CountingTransport([
            httpx.Response(500),
            httpx.Response(200),
        ])
        transport = RetryTransport(inner, max_retries=3, backoff_base=0.0)
        response = transport.handle_request(httpx.Request("GET", "https://example.com"))
        assert response.status_code == 200
        assert inner.call_count == 2

    def test_retries_on_429_then_succeeds(self) -> None:
        inner = _CountingTransport([
            httpx.Response(429, headers={"retry-after": "0"}),
            httpx.Response(200),
        ])
        transport = RetryTransport(inner, max_retries=3, backoff_base=0.0)
        response = transport.handle_request(httpx.Request("GET", "https://example.com"))
        assert response.status_code == 200

    def test_exhausts_retries_returns_last_response(self) -> None:
        inner = _CountingTransport([
            httpx.Response(503),
            httpx.Response(503),
            httpx.Response(503),
        ])
        transport = RetryTransport(inner, max_retries=3, backoff_base=0.0)
        response = transport.handle_request(httpx.Request("GET", "https://example.com"))
        assert response.status_code == 503
        assert inner.call_count == 3

    def test_timeout_raises_nexus_timeout(self) -> None:
        inner = _FailingTransport(httpx.ReadTimeout("timed out"))
        transport = RetryTransport(inner, max_retries=2, backoff_base=0.0)
        with pytest.raises(NexusTimeoutError):
            transport.handle_request(httpx.Request("GET", "https://example.com"))
        assert inner.call_count == 2

    def test_connect_error_raises_nexus_connection(self) -> None:
        inner = _FailingTransport(httpx.ConnectError("refused"))
        transport = RetryTransport(inner, max_retries=2, backoff_base=0.0)
        with pytest.raises(NexusConnectionError):
            transport.handle_request(httpx.Request("GET", "https://example.com"))
        assert inner.call_count == 2

    def test_non_retryable_status_returned_immediately(self) -> None:
        inner = _CountingTransport([httpx.Response(404)])
        transport = RetryTransport(inner, max_retries=3, backoff_base=0.0)
        response = transport.handle_request(httpx.Request("GET", "https://example.com"))
        assert response.status_code == 404
        assert inner.call_count == 1
