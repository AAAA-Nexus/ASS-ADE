# Extracted from C:/!ass-ade/tests/test_mcp_server_streaming.py:208
# Component id: sy.source.ass_ade.complete
from __future__ import annotations

__version__ = "0.1.0"

def complete(self, request):
    idx = min(self._idx, len(self._responses) - 1)
    self._idx += 1
    return self._responses[idx]
