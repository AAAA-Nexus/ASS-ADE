# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_raise_for_status.py:5
# Component id: at.source.ass_ade.raise_for_status
__version__ = "0.1.0"

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
