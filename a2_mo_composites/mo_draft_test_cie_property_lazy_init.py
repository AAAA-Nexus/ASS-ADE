# Extracted from C:/!ass-ade/tests/test_phase_engines.py:648
# Component id: mo.source.ass_ade.test_cie_property_lazy_init
from __future__ import annotations

__version__ = "0.1.0"

def test_cie_property_lazy_init(self):
    orch = self._make()
    cie = orch.cie
    assert cie is not None
