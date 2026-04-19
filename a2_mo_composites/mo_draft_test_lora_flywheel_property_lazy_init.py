# Extracted from C:/!ass-ade/tests/test_phase_engines.py:653
# Component id: mo.source.ass_ade.test_lora_flywheel_property_lazy_init
from __future__ import annotations

__version__ = "0.1.0"

def test_lora_flywheel_property_lazy_init(self):
    orch = self._make()
    fly = orch.lora_flywheel
    assert fly is not None
