# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_alert.py:7
# Component id: mo.source.a2_mo_composites.alert
from __future__ import annotations

__version__ = "0.1.0"

class Alert:
    kind: str
    severity: str
    payload: dict
    ts: str
    cooldown_skipped: bool = False
