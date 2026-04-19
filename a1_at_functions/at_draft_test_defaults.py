# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_defaults.py:7
# Component id: at.source.a1_at_functions.test_defaults
from __future__ import annotations

__version__ = "0.1.0"

def test_defaults(self):
    r = CompletionRequest(messages=[Message(role="user", content="hi")])
    assert r.temperature == 0.0
    assert r.max_tokens == 4096
    assert r.tools == []
    assert r.model is None
