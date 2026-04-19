# Extracted from C:/!ass-ade/tests/test_agent.py:158
# Component id: at.source.ass_ade.complete
from __future__ import annotations

__version__ = "0.1.0"

def complete(self, request: CompletionRequest) -> CompletionResponse:  # noqa: ARG002
    idx = min(self._call_count, len(self._responses) - 1)
    self._call_count += 1
    return self._responses[idx]
