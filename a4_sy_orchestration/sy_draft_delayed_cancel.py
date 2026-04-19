# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a4_sy_orchestration/sy_draft_testmcpcancellation.py:121
# Component id: sy.source.a4_sy_orchestration.delayed_cancel
from __future__ import annotations

__version__ = "0.1.0"

def delayed_cancel():
    time.sleep(0.05)
    ctx.cancel()
