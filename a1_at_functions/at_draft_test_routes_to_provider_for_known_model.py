# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_routes_to_provider_for_known_model.py:7
# Component id: at.source.a1_at_functions.test_routes_to_provider_for_known_model
from __future__ import annotations

__version__ = "0.1.0"

def test_routes_to_provider_for_known_model(self):
    from ass_ade.engine.provider import MultiProvider
    from ass_ade.engine.types import CompletionRequest, Message
    a = self._make_provider("a")
    b = self._make_provider("b")
    mp = MultiProvider(
        providers={"a": a, "b": b},
        model_to_provider={"model-a": "a", "model-b": "b"},
        fallback_order=["a", "b"],
    )
    req = CompletionRequest(messages=[Message(role="user", content="hi")], tools=[], model="model-b")
    mp.complete(req)
    b.complete.assert_called_once()
    a.complete.assert_not_called()
    assert mp.last_provider_name == "b"
