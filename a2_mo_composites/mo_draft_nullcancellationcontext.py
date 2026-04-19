# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nullcancellationcontext.py:7
# Component id: mo.source.a2_mo_composites.nullcancellationcontext
from __future__ import annotations

__version__ = "0.1.0"

class NullCancellationContext(CancellationContext):
    """No-op cancellation context for operations that don't support cancellation."""

    def cancel(self) -> None:
        """Do nothing."""
        pass

    def check(self) -> bool:
        """Always return False — never cancelled."""
        return False
