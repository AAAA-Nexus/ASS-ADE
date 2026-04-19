# Extracted from C:/!ass-ade/tests/test_free_providers.py:378
# Component id: mo.source.ass_ade.testmultiprovider
from __future__ import annotations

__version__ = "0.1.0"

class TestMultiProvider:
    def _make_provider(self, name: str, fails: bool = False):
        p = MagicMock()
        p.name = name
        if fails:
            p.complete.side_effect = httpx.ConnectError("boom")
        else:
            p.complete.return_value = MagicMock(
                message=MagicMock(content=f"from-{name}", tool_calls=[]),
                usage={"input_tokens": 1, "output_tokens": 1},
            )
        return p

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

    def test_all_providers_fail_raises(self):
        from ass_ade.engine.provider import MultiProvider
        from ass_ade.engine.types import CompletionRequest, Message
        p1 = self._make_provider("p1", fails=True)
        p2 = self._make_provider("p2", fails=True)
        mp = MultiProvider(
            providers={"p1": p1, "p2": p2},
            model_to_provider={},
            fallback_order=["p1", "p2"],
        )
        req = CompletionRequest(messages=[Message(role="user", content="hi")], tools=[], model=None)
        with pytest.raises(httpx.HTTPError):
            mp.complete(req)

    def test_register_adds_provider_at_runtime(self):
        from ass_ade.engine.provider import MultiProvider
        a = self._make_provider("a")
        mp = MultiProvider(providers={"a": a}, fallback_order=["a"])
        b = self._make_provider("b")
        mp.register("b", b, models=["model-b-1"])
        assert "b" in mp.providers
        assert "b" in mp._fallback_order
        assert mp._model_to_provider["model-b-1"] == "b"

    def test_close_forwards_to_all_underlying(self):
        from ass_ade.engine.provider import MultiProvider
        a = self._make_provider("a")
        b = self._make_provider("b")
        mp = MultiProvider(providers={"a": a, "b": b}, fallback_order=["a", "b"])
        mp.close()
        a.close.assert_called_once()
        b.close.assert_called_once()
