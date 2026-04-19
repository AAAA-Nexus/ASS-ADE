# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexuserror.py:7
# Component id: mo.source.a2_mo_composites.nexuserror
from __future__ import annotations

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
