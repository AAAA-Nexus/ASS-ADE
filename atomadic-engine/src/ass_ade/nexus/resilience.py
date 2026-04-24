"""Resilient httpx transports for AAAA-Nexus client hardening.

Composable transport wrappers that implement:
  - Exponential-backoff retry with jitter (429 / 5xx)
  - Circuit breaker (trip after N consecutive failures)
  - Clean timeout enforcement
  - Cooperative cancellation support

All transports implement ``httpx.BaseTransport`` so they can be stacked.
"""

from __future__ import annotations

import random
import time
from typing import TYPE_CHECKING

import httpx

from ass_ade.nexus.errors import (
    NexusCircuitOpen,
    NexusConnectionError,
    NexusServerError,
    NexusTimeoutError,
)

if TYPE_CHECKING:
    from ass_ade.mcp.cancellation import CancellationContext


class RetryTransport(httpx.BaseTransport):
    """Retry on 429 and 5xx with exponential backoff + jitter.

    Respects the ``Retry-After`` response header when present.
    Supports cooperative cancellation via optional CancellationContext.
    """

    RETRYABLE_STATUS = frozenset({429, 500, 502, 503, 504})

    def __init__(
        self,
        wrapped: httpx.BaseTransport | None = None,
        *,
        max_retries: int = 3,
        backoff_base: float = 0.5,
        backoff_max: float = 8.0,
        cancellation_context: CancellationContext | None = None,
    ) -> None:
        self._wrapped = wrapped or httpx.HTTPTransport()
        self._max_retries = max(1, max_retries)
        self._backoff_base = backoff_base
        self._backoff_max = backoff_max
        self._cancellation_context = cancellation_context

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        last_response: httpx.Response | None = None
        last_exc: Exception | None = None

        for attempt in range(self._max_retries):
            # Check for cancellation before each attempt
            if self._cancellation_context and self._cancellation_context.check():
                raise NexusConnectionError(
                    "Request cancelled during retry loop",
                    endpoint=str(request.url),
                )

            try:
                response = self._wrapped.handle_request(request)
            except httpx.TimeoutException as exc:
                last_exc = exc
                if attempt < self._max_retries - 1:
                    self._sleep(attempt)
                    continue
                raise NexusTimeoutError(
                    f"Timeout after {self._max_retries} attempts: {exc}",
                    endpoint=str(request.url),
                ) from exc
            except httpx.ConnectError as exc:
                last_exc = exc
                if attempt < self._max_retries - 1:
                    self._sleep(attempt)
                    continue
                raise NexusConnectionError(
                    f"Connection failed after {self._max_retries} attempts: {exc}",
                    endpoint=str(request.url),
                ) from exc

            if response.status_code not in self.RETRYABLE_STATUS:
                return response

            last_response = response

            if attempt < self._max_retries - 1:
                retry_after = self._parse_retry_after(response)
                self._sleep(attempt, retry_after)

        # All retries exhausted — return the last response so the caller can inspect
        if last_response is not None:
            return last_response

        if last_exc is not None:
            raise NexusConnectionError(
                f"All {self._max_retries} retries exhausted",
                endpoint=str(request.url),
            ) from last_exc

        raise NexusServerError("Retries exhausted with no response", endpoint=str(request.url))

    def _sleep(self, attempt: int, retry_after: float | None = None) -> None:
        if retry_after is not None and retry_after > 0:
            time.sleep(min(retry_after, self._backoff_max))
            return
        delay = min(self._backoff_base * (2**attempt), self._backoff_max)
        jitter = random.uniform(0, delay * 0.25)  # noqa: S311
        time.sleep(delay + jitter)

    @staticmethod
    def _parse_retry_after(response: httpx.Response) -> float | None:
        raw = response.headers.get("retry-after")
        if raw is None:
            return None
        try:
            return float(raw)
        except (ValueError, TypeError):
            return None

    def close(self) -> None:
        self._wrapped.close()


class CircuitBreakerTransport(httpx.BaseTransport):
    """Trip after ``failure_threshold`` consecutive failures within ``window_s``.

    Once open, all calls raise ``NexusCircuitOpen`` until ``recovery_s``
    elapses, then a single probe is allowed (half-open state).
    """

    def __init__(
        self,
        wrapped: httpx.BaseTransport | None = None,
        *,
        failure_threshold: int = 5,
        window_s: float = 60.0,
        recovery_s: float = 30.0,
    ) -> None:
        self._wrapped = wrapped or httpx.HTTPTransport()
        self._failure_threshold = failure_threshold
        self._window_s = window_s
        self._recovery_s = recovery_s
        self._failures: list[float] = []
        self._open_since: float | None = None

    @property
    def is_open(self) -> bool:
        if self._open_since is None:
            return False
        if time.monotonic() - self._open_since >= self._recovery_s:
            return False  # half-open: allow a probe
        return True

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        if self.is_open:
            raise NexusCircuitOpen(
                "Circuit breaker is open — calls blocked temporarily",
                endpoint=str(request.url),
            )

        try:
            response = self._wrapped.handle_request(request)
        except Exception:
            self._record_failure()
            raise

        if response.status_code >= 500:
            self._record_failure()
        else:
            self._reset()

        return response

    def _record_failure(self) -> None:
        now = time.monotonic()
        self._failures = [t for t in self._failures if now - t < self._window_s]
        self._failures.append(now)
        if len(self._failures) >= self._failure_threshold:
            self._open_since = now

    def _reset(self) -> None:
        self._failures.clear()
        self._open_since = None

    def close(self) -> None:
        self._wrapped.close()


def build_resilient_transport(
    *,
    max_retries: int = 3,
    backoff_base: float = 0.5,
    circuit_failure_threshold: int = 5,
    circuit_window_s: float = 60.0,
    circuit_recovery_s: float = 30.0,
    cancellation_context: CancellationContext | None = None,
) -> httpx.BaseTransport:
    """Build a composed transport stack: CircuitBreaker (outer) → Retry (middle) → HTTP (inner).

    Requests traverse: CircuitBreaker → Retry → HTTP.
    
    Args:
        cancellation_context: Optional context for cooperative cancellation support.
            If provided, the retry transport will check for cancellation between
            retry attempts and abort with NexusConnectionError if cancelled.
    """
    base = httpx.HTTPTransport()
    retrying = RetryTransport(
        base,
        max_retries=max_retries,
        backoff_base=backoff_base,
        cancellation_context=cancellation_context,
    )
    return CircuitBreakerTransport(
        retrying,
        failure_threshold=circuit_failure_threshold,
        window_s=circuit_window_s,
        recovery_s=circuit_recovery_s,
    )
