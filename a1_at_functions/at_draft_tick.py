# Extracted from C:/!ass-ade/src/ass_ade/agent/lora_flywheel.py:191
# Component id: at.source.ass_ade.tick
from __future__ import annotations

__version__ = "0.1.0"

def tick(self) -> BatchResult | None:
    """Advance step counter. Returns BatchResult if batch was submitted."""
    self._step_count += 1
    if self._step_count % self._batch_interval == 0 and self._pending:
        return self.contribute_batch()
    return None
