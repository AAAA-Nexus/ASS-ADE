# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testcompletionresponse.py:7
# Component id: mo.source.a2_mo_composites.testcompletionresponse
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
