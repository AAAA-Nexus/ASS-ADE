# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_lse_property_lazy_init.py:7
# Component id: at.source.a1_at_functions.test_lse_property_lazy_init
from __future__ import annotations

__version__ = "0.1.0"

def test_lse_property_lazy_init(self):
    orch = self._make()
    assert orch._lse is None
    lse = orch.lse
    assert lse is not None
    assert orch._lse is lse  # cached
