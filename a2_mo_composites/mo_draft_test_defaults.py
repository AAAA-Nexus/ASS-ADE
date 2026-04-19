# Extracted from C:/!ass-ade/tests/test_engine.py:51
# Component id: mo.source.ass_ade.test_defaults
from __future__ import annotations

__version__ = "0.1.0"

def test_defaults(self):
    r = CompletionRequest(messages=[Message(role="user", content="hi")])
    assert r.temperature == 0.0
    assert r.max_tokens == 4096
    assert r.tools == []
    assert r.model is None
