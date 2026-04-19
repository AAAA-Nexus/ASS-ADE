# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_lora_capture_fix.py:7
# Component id: at.source.a1_at_functions.lora_capture_fix
from __future__ import annotations

__version__ = "0.1.0"

def lora_capture_fix(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
    """Alias for lora_buffer_capture — single (bad, good) sample."""
    return self.lora_buffer_capture(*args, **kwargs)
