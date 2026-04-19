# Extracted from C:/!ass-ade/tests/test_phase1_integration.py:63
# Component id: at.source.ass_ade.test_sam_pipeline_passes_intent_and_impl
from __future__ import annotations

__version__ = "0.1.0"

def test_sam_pipeline_passes_intent_and_impl(self):
    nexus = _make_nexus_mock()
    gates = QualityGates(nexus, config={})
    with patch("ass_ade.context_memory.vector_embed", return_value=[0.5, 0.5, 0.5]):
        results = gates.run_pipeline(
            prompt="add input validation",
            output="def f(x): assert x",
            intent="add input validation",
            impl="def f(x): assert x",
        )
    sam_result = next((r for r in results if r.gate == "sam"), None)
    assert sam_result is not None
    assert sam_result.details is not None
    assert "trs" in sam_result.details
    assert "g23" in sam_result.details
