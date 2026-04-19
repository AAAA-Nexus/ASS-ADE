# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_handle_request.py:7
# Component id: at.source.a1_at_functions.handle_request
from __future__ import annotations

__version__ = "0.1.0"

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
