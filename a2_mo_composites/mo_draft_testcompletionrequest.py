# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testcompletionrequest.py:7
# Component id: mo.source.a2_mo_composites.testcompletionrequest
from __future__ import annotations

__version__ = "0.1.0"

class TestCompletionRequest:
    def test_defaults(self):
        r = CompletionRequest(messages=[Message(role="user", content="hi")])
        assert r.temperature == 0.0
        assert r.max_tokens == 4096
        assert r.tools == []
        assert r.model is None
