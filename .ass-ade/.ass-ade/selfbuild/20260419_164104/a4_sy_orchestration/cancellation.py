"""Cancellation context for cooperative cancellation in MCP requests.

Allows long-running operations to check if they have been cancelled and
respond cooperatively by halting work and returning early.
"""

from __future__ import annotations

import threading
from typing import Optional


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


class NullCancellationContext(CancellationContext):
    """No-op cancellation context for operations that don't support cancellation."""

    def cancel(self) -> None:
        """Do nothing."""
        pass

    def check(self) -> bool:
        """Always return False — never cancelled."""
        return False


def get_null_context() -> CancellationContext:
    """Get a singleton no-op cancellation context."""
    return NullCancellationContext()
