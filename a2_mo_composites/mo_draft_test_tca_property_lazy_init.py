# Extracted from C:/!ass-ade/tests/test_phase_engines.py:643
# Component id: mo.source.ass_ade.test_tca_property_lazy_init
from __future__ import annotations

__version__ = "0.1.0"

def test_tca_property_lazy_init(self):
    orch = self._make()
    tca = orch.tca
    assert tca is not None
