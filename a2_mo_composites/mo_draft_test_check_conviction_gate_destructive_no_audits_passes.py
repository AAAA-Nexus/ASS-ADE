# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testengineorchestratorphase15.py:41
# Component id: mo.source.a2_mo_composites.test_check_conviction_gate_destructive_no_audits_passes
from __future__ import annotations

__version__ = "0.1.0"

def test_check_conviction_gate_destructive_no_audits_passes(self):
    orch = self._make()
    # write_file with 0 audits → should not block (no audit history yet)
    blocked = orch.check_conviction_gate("write_file", {})
    assert blocked is False
