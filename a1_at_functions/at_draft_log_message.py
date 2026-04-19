# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_log_message.py:7
# Component id: at.source.a1_at_functions.log_message
from __future__ import annotations

__version__ = "0.1.0"

def log_message(self, fmt: str, *args: Any) -> None:
    _log.debug(fmt, *args)
