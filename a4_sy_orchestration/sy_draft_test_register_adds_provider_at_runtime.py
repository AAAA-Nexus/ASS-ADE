# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_free_providers.py:452
# Component id: sy.source.ass_ade.test_register_adds_provider_at_runtime
__version__ = "0.1.0"

    def test_register_adds_provider_at_runtime(self):
        from ass_ade.engine.provider import MultiProvider
        a = self._make_provider("a")
        mp = MultiProvider(providers={"a": a}, fallback_order=["a"])
        b = self._make_provider("b")
        mp.register("b", b, models=["model-b-1"])
        assert "b" in mp.providers
        assert "b" in mp._fallback_order
        assert mp._model_to_provider["model-b-1"] == "b"
