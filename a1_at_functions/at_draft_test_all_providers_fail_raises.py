# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_free_providers.py:438
# Component id: at.source.ass_ade.test_all_providers_fail_raises
__version__ = "0.1.0"

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
