# Extracted from C:/!ass-ade/tests/test_engine.py:59
# Component id: mo.source.ass_ade.testcompletionresponse
from __future__ import annotations

__version__ = "0.1.0"

class TestCompletionResponse:
    def test_basic(self):
        r = CompletionResponse(
            message=Message(role="assistant", content="done"),
            finish_reason="stop",
        )
        assert r.finish_reason == "stop"
        assert r.model is None
