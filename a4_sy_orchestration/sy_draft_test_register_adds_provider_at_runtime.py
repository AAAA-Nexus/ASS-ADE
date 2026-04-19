# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testmultiprovider.py:81
# Component id: sy.source.a2_mo_composites.test_register_adds_provider_at_runtime
from __future__ import annotations

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
