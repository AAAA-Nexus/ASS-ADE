# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testengineorchestratorphase15.py:47
# Component id: mo.source.a2_mo_composites.test_engine_report_includes_new_engines_after_init
from __future__ import annotations

__version__ = "0.1.0"

def test_engine_report_includes_new_engines_after_init(self):
    orch = self._make()
    # Touch the new engines to init them
    _ = orch.lse
    _ = orch.tca
    _ = orch.cie
    _ = orch.lora_flywheel
    rep = orch.engine_report()
    assert "lse" in rep
    assert "tca" in rep
    assert "cie" in rep
    assert "lora_flywheel" in rep
