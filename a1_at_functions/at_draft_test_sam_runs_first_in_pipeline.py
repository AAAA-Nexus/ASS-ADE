# Extracted from C:/!ass-ade/tests/test_phase1_integration.py:53
# Component id: at.source.ass_ade.test_sam_runs_first_in_pipeline
from __future__ import annotations

__version__ = "0.1.0"

def test_sam_runs_first_in_pipeline(self):
    nexus = _make_nexus_mock()
    gates = QualityGates(nexus, config={})
    with patch("ass_ade.context_memory.vector_embed", return_value=[0.1, 0.2, 0.3]):
        results = gates.run_pipeline(prompt="build a function", output="def x(): pass")
    gate_names = [r.gate for r in results]
    assert "sam" in gate_names, f"SAM missing from pipeline: {gate_names}"
    # SAM must be the very first gate
    assert gate_names[0] == "sam"
