# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testengineorchestratorphase15.py:25
# Component id: mo.source.a2_mo_composites.test_cie_property_lazy_init
from __future__ import annotations

__version__ = "0.1.0"

def test_cie_property_lazy_init(self):
    orch = self._make()
    cie = orch.cie
    assert cie is not None
