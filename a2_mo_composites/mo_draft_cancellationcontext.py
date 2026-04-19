# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_cancellationcontext.py:7
# Component id: mo.source.a2_mo_composites.cancellationcontext
from __future__ import annotations

__version__ = "0.1.0"

class CancellationContext:
    """Thread-safe context for signaling cancellation to in-flight operations.

    Long-running tools can periodically call check() to see if a cancellation
    request has been issued. When check() returns True, the tool should clean
    up and return promptly.
    """

    def __init__(self) -> None:
        self._cancelled = False
        self._lock = threading.Lock()

    def cancel(self) -> None:
        """Mark this context as cancelled."""
        with self._lock:
            self._cancelled = True

    def check(self) -> bool:
        """Check if cancellation has been requested.

        Returns True if cancel() was called, False otherwise.
        Long-running operations should call this periodically and exit early
        if it returns True.
        """
        with self._lock:
            return self._cancelled

    @property
    def is_cancelled(self) -> bool:
        """Alias for check()."""
        return self.check()
