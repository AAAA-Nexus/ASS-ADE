# Extracted from C:/!ass-ade/tests/test_phase_engines.py:664
# Component id: mo.source.ass_ade.test_check_conviction_gate_destructive_no_audits_passes
from __future__ import annotations

__version__ = "0.1.0"

def test_check_conviction_gate_destructive_no_audits_passes(self):
    orch = self._make()
    # write_file with 0 audits → should not block (no audit history yet)
    blocked = orch.check_conviction_gate("write_file", {})
    assert blocked is False
