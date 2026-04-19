# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_free_providers.py:462
# Component id: at.source.ass_ade.test_close_forwards_to_all_underlying
__version__ = "0.1.0"

    def test_close_forwards_to_all_underlying(self):
        from ass_ade.engine.provider import MultiProvider
        a = self._make_provider("a")
        b = self._make_provider("b")
        mp = MultiProvider(providers={"a": a, "b": b}, fallback_order=["a", "b"])
        mp.close()
        a.close.assert_called_once()
        b.close.assert_called_once()
