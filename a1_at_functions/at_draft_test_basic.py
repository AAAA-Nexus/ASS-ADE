# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_basic.py:7
# Component id: at.source.a1_at_functions.test_basic
from __future__ import annotations

__version__ = "0.1.0"

def test_basic(self):
    r = CompletionResponse(
        message=Message(role="assistant", content="done"),
        finish_reason="stop",
    )
    assert r.finish_reason == "stop"
    assert r.model is None
