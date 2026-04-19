# Extracted from C:/!ass-ade/tests/test_engine.py:60
# Component id: mo.source.ass_ade.test_basic
from __future__ import annotations

__version__ = "0.1.0"

def test_basic(self):
    r = CompletionResponse(
        message=Message(role="assistant", content="done"),
        finish_reason="stop",
    )
    assert r.finish_reason == "stop"
    assert r.model is None
