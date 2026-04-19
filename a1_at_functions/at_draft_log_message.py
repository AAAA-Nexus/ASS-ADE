# Extracted from C:/!ass-ade/scripts/lora_training/serve_lora.py:108
# Component id: at.source.ass_ade.log_message
from __future__ import annotations

__version__ = "0.1.0"

def log_message(self, fmt: str, *args: Any) -> None:
    _log.debug(fmt, *args)
