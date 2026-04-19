# Extracted from C:/!ass-ade/tests/test_mcp_cancellation.py:186
# Component id: sy.source.ass_ade.delayed_cancel
from __future__ import annotations

__version__ = "0.1.0"

def delayed_cancel():
    time.sleep(0.05)
    ctx.cancel()
