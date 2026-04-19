# Extracted from C:/!ass-ade/src/ass_ade/nexus/client.py:1456
# Component id: mo.source.ass_ade.lora_capture_fix
from __future__ import annotations

__version__ = "0.1.0"

def lora_capture_fix(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
    """Alias for lora_buffer_capture — single (bad, good) sample."""
    return self.lora_buffer_capture(*args, **kwargs)
