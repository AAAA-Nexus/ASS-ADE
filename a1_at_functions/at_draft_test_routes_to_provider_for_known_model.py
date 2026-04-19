# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testmultiprovider.py:18
# Component id: at.source.ass_ade.test_routes_to_provider_for_known_model
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
