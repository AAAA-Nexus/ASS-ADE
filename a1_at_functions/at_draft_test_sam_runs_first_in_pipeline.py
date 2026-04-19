# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_sam_runs_first_in_pipeline.py:7
# Component id: at.source.a1_at_functions.test_sam_runs_first_in_pipeline
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
