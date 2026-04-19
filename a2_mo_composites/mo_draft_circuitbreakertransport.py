# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/resilience.py:131
# Component id: mo.source.ass_ade.circuitbreakertransport
__version__ = "0.1.0"

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
