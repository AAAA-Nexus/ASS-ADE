# Extracted from C:/!ass-ade/src/ass_ade/mcp/cancellation.py:58
# Component id: sy.source.ass_ade.get_null_context
from __future__ import annotations

__version__ = "0.1.0"

def get_null_context() -> CancellationContext:
    """Get a singleton no-op cancellation context."""
    return NullCancellationContext()
