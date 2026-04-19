# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_gate_sam_fail_open_on_exception.py:7
# Component id: at.source.a1_at_functions.test_gate_sam_fail_open_on_exception
from __future__ import annotations

__version__ = "0.1.0"

def test_gate_sam_fail_open_on_exception(self):
    from ass_ade.agent.gates import QualityGates
    broken_nexus = MagicMock()
    broken_nexus.trust_score.side_effect = RuntimeError("boom")
    gates = QualityGates(nexus_client=broken_nexus, config={})
    # Should not raise — context_memory may also raise; patch it
    with patch("ass_ade.context_memory.vector_embed", return_value=[0.1, 0.2]):
        result = gates.gate_sam(target="x")
    # Either None (fail-open) or a dict
    assert result is None or isinstance(result, dict)
