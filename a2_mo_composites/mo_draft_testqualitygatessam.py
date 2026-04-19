# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testqualitygatessam.py:7
# Component id: mo.source.a2_mo_composites.testqualitygatessam
from __future__ import annotations

__version__ = "0.1.0"

class TestQualityGatesSAM:
    def _make_gates(self):
        from ass_ade.agent.gates import QualityGates
        nexus = MagicMock()
        nexus.trust_score.return_value = MagicMock(score=0.9)
        nexus.security_shield.return_value = MagicMock(blocked=False)
        return QualityGates(nexus_client=nexus, config={})

    def test_gate_sam_returns_dict(self):
        gates = self._make_gates()
        result = gates.gate_sam(target="test_target")
        assert result is not None
        assert "trs" in result
        assert "g23" in result
        assert "composite" in result
        assert "passed" in result

    def test_gate_sam_logs_to_gate_log(self):
        gates = self._make_gates()
        gates.gate_sam(target="x")
        assert any(g.gate == "sam" for g in gates.gate_log)

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
