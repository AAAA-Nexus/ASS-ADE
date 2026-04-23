"""Tests for resilient httpx transports — retry, circuit breaker."""

from __future__ import annotations

import httpx
import pytest

from ass_ade.nexus.errors import NexusCircuitOpen, NexusConnectionError, NexusTimeoutError
from ass_ade.nexus.resilience import (
    CircuitBreakerTransport,
    RetryTransport,
    build_resilient_transport,
)

# ── Helpers ──────────────────────────────────────────────────────────────────

class _CountingTransport(httpx.BaseTransport):
    """Returns a configurable sequence of responses."""

    def __init__(self, responses: list[httpx.Response]) -> None:
        self._responses = list(responses)
        self._index = 0
        self.call_count = 0

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        self.call_count += 1
        idx = min(self._index, len(self._responses) - 1)
        self._index += 1
        return self._responses[idx]


class _FailingTransport(httpx.BaseTransport):
    """Raises on every call."""

    def __init__(self, exc: Exception) -> None:
        self._exc = exc
        self.call_count = 0

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        self.call_count += 1
        raise self._exc


# ── RetryTransport tests ────────────────────────────────────────────────────

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


# ── CircuitBreakerTransport tests ───────────────────────────────────────────

class TestCircuitBreakerTransport:
    def test_success_keeps_circuit_closed(self) -> None:
        inner = _CountingTransport([httpx.Response(200)] * 10)
        cb = CircuitBreakerTransport(inner, failure_threshold=3, window_s=60, recovery_s=0.1)
        for _ in range(5):
            resp = cb.handle_request(httpx.Request("GET", "https://example.com"))
            assert resp.status_code == 200
        assert not cb.is_open

    def test_consecutive_5xx_trips_circuit(self) -> None:
        inner = _CountingTransport([httpx.Response(500)] * 10)
        cb = CircuitBreakerTransport(inner, failure_threshold=3, window_s=60, recovery_s=30)
        for _ in range(3):
            cb.handle_request(httpx.Request("GET", "https://example.com"))
        assert cb.is_open

    def test_open_circuit_raises_immediately(self) -> None:
        inner = _CountingTransport([httpx.Response(500)] * 10)
        cb = CircuitBreakerTransport(inner, failure_threshold=2, window_s=60, recovery_s=30)
        for _ in range(2):
            cb.handle_request(httpx.Request("GET", "https://example.com"))
        with pytest.raises(NexusCircuitOpen):
            cb.handle_request(httpx.Request("GET", "https://example.com"))

    def test_success_after_failures_resets(self) -> None:
        responses = [httpx.Response(500), httpx.Response(200)]
        inner = _CountingTransport(responses)
        cb = CircuitBreakerTransport(inner, failure_threshold=3, window_s=60, recovery_s=0.1)
        cb.handle_request(httpx.Request("GET", "https://example.com"))  # 500
        cb.handle_request(httpx.Request("GET", "https://example.com"))  # 200 resets
        assert not cb.is_open


# ── build_resilient_transport ────────────────────────────────────────────────

class TestBuildResilientTransport:
    def test_returns_circuit_breaker_wrapping_retry(self) -> None:
        transport = build_resilient_transport(max_retries=2)
        assert isinstance(transport, CircuitBreakerTransport)
        assert isinstance(transport._wrapped, RetryTransport)
