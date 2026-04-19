# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/errors.py:10
# Component id: mo.source.ass_ade.nexuserror
__version__ = "0.1.0"

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
