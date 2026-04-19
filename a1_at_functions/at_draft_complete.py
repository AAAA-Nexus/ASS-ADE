# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_complete.py:7
# Component id: at.source.a1_at_functions.complete
from __future__ import annotations

__version__ = "0.1.0"

def complete(self, request: CompletionRequest) -> CompletionResponse:  # noqa: ARG002
    idx = min(self._call_count, len(self._responses) - 1)
    self._call_count += 1
    return self._responses[idx]
