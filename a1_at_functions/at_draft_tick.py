# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_tick.py:7
# Component id: at.source.a1_at_functions.tick
from __future__ import annotations

__version__ = "0.1.0"

def tick(self) -> BatchResult | None:
    """Advance step counter. Returns BatchResult if batch was submitted."""
    self._step_count += 1
    if self._step_count % self._batch_interval == 0 and self._pending:
        return self.contribute_batch()
    return None
