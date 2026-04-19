# Extracted from C:/!ass-ade/tests/test_phase_engines.py:636
# Component id: mo.source.ass_ade.test_lse_property_lazy_init
from __future__ import annotations

__version__ = "0.1.0"

def test_lse_property_lazy_init(self):
    orch = self._make()
    assert orch._lse is None
    lse = orch.lse
    assert lse is not None
    assert orch._lse is lse  # cached
