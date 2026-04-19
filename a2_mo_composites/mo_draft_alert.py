# Extracted from C:/!ass-ade/src/ass_ade/agent/bas.py:16
# Component id: mo.source.ass_ade.alert
from __future__ import annotations

__version__ = "0.1.0"

class Alert:
    kind: str
    severity: str
    payload: dict
    ts: str
    cooldown_skipped: bool = False
