# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_retrytransport.py:7
# Component id: mo.source.a2_mo_composites.retrytransport
from __future__ import annotations

__version__ = "0.1.0"

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
