# Extracted from C:/!ass-ade/tests/test_mcp_cancellation.py:56
# Component id: sy.source.ass_ade.cancel_once
from __future__ import annotations

__version__ = "0.1.0"

def cancel_once():
    time.sleep(0.01)
    ctx.cancel()
