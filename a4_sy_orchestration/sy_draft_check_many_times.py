# Extracted from C:/!ass-ade/tests/test_mcp_cancellation.py:51
# Component id: sy.source.ass_ade.check_many_times
from __future__ import annotations

__version__ = "0.1.0"

def check_many_times():
    for _ in range(100):
        results.append(ctx.check())
        time.sleep(0.001)
