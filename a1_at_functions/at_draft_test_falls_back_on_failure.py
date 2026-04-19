# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_falls_back_on_failure.py:7
# Component id: at.source.a1_at_functions.test_falls_back_on_failure
from __future__ import annotations

__version__ = "0.1.0"

def test_falls_back_on_failure(self):
    from ass_ade.engine.provider import MultiProvider
    from ass_ade.engine.types import CompletionRequest, Message
    failing = self._make_provider("failing", fails=True)
    backup = self._make_provider("backup")
    mp = MultiProvider(
        providers={"failing": failing, "backup": backup},
        model_to_provider={"model-x": "failing"},
        fallback_order=["failing", "backup"],
    )
    req = CompletionRequest(messages=[Message(role="user", content="hi")], tools=[], model="model-x")
    resp = mp.complete(req)
    assert mp.last_provider_name == "backup"
    assert resp.message.content == "from-backup"
    failing.complete.assert_called_once()
    backup.complete.assert_called_once()
