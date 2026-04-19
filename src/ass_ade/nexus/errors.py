"""Typed exception hierarchy for AAAA-Nexus API interactions.

Every exception carries enough context for CLI commands to produce
actionable, user-friendly error messages without leaking internals.
"""

from __future__ import annotations


class NexusError(Exception):
    """Base exception for all AAAA-Nexus client errors."""

    def __init__(
        self,
        detail: str,
        *,
        status_code: int | None = None,
        endpoint: str | None = None,
        retry_after: float | None = None,
    ) -> None:
        self.detail = detail
        self.status_code = status_code
        self.endpoint = endpoint
        self.retry_after = retry_after
        super().__init__(detail)


class NexusConnectionError(NexusError):
    """Network unreachable, DNS failure, or TLS error."""


class NexusTimeoutError(NexusError):
    """Request exceeded the configured timeout."""


class NexusAuthError(NexusError):
    """Authentication or authorisation failure (401/403)."""


class NexusPaymentRequired(NexusError):
    """Payment required — x402 or credit-pack exhausted (402)."""


class NexusRateLimited(NexusError):
    """Rate limit exceeded (429).  Check ``retry_after``."""


class NexusServerError(NexusError):
    """Server-side error (5xx)."""


class NexusValidationError(NexusError):
    """Input rejected by the API (422)."""


class NexusCircuitOpen(NexusError):
    """Client-side circuit breaker is open — calls are blocked temporarily."""


# ── Mapping helper ────────────────────────────────────────────────────────────

_STATUS_MAP: dict[int, type[NexusError]] = {
    401: NexusAuthError,
    403: NexusAuthError,
    402: NexusPaymentRequired,
    422: NexusValidationError,
    429: NexusRateLimited,
}


def raise_for_status(status_code: int, *, endpoint: str = "", detail: str = "", retry_after: float | None = None) -> None:
    """Raise the appropriate typed exception for a non-2xx status code.

    Does nothing when ``status_code`` is in the 2xx range.
    """
    if 200 <= status_code < 300:
        return

    exc_cls = _STATUS_MAP.get(status_code)
    if exc_cls is None and 500 <= status_code < 600:
        exc_cls = NexusServerError
    if exc_cls is None:
        exc_cls = NexusError

    msg = detail or f"HTTP {status_code} from {endpoint or 'unknown'}"
    raise exc_cls(msg, status_code=status_code, endpoint=endpoint, retry_after=retry_after)
