"""Tier a1 — assimilated function 'get_null_context'

Assimilated from: cancellation.py:58-60
"""

from __future__ import annotations


# --- assimilated symbol ---
def get_null_context() -> CancellationContext:
    """Get a singleton no-op cancellation context."""
    return NullCancellationContext()

