# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_unknown_model_uses_fallback_order.py:7
# Component id: at.source.a1_at_functions.test_unknown_model_uses_fallback_order
from __future__ import annotations

__version__ = "0.1.0"

def test_unknown_model_uses_fallback_order(self):
    from ass_ade.engine.provider import MultiProvider
    from ass_ade.engine.types import CompletionRequest, Message
    a = self._make_provider("a")
    b = self._make_provider("b")
    mp = MultiProvider(
        providers={"a": a, "b": b},
        model_to_provider={},
        fallback_order=["b", "a"],
    )
    req = CompletionRequest(messages=[Message(role="user", content="hi")], tools=[], model="unknown")
    mp.complete(req)
    b.complete.assert_called_once()  # first in fallback
