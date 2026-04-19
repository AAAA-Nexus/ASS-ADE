# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_close_forwards_to_all_underlying.py:7
# Component id: at.source.a1_at_functions.test_close_forwards_to_all_underlying
from __future__ import annotations

__version__ = "0.1.0"

def test_close_forwards_to_all_underlying(self):
    from ass_ade.engine.provider import MultiProvider
    a = self._make_provider("a")
    b = self._make_provider("b")
    mp = MultiProvider(providers={"a": a, "b": b}, fallback_order=["a", "b"])
    mp.close()
    a.close.assert_called_once()
    b.close.assert_called_once()
