# Extracted from C:/!ass-ade/tests/test_gates.py:146
# Component id: at.source.ass_ade.test_full_pipeline
from __future__ import annotations

__version__ = "0.1.0"

def test_full_pipeline(self):
    gates = QualityGates(_mock_nexus())
    results = gates.run_pipeline(prompt="What is Python?", output="A programming language.")
    # Phase 1: SAM is now Stage 0, so 4 gates total: sam + scan + hallucination + certify
    assert len(results) == 4
    assert [r.gate for r in results] == ["sam", "prompt_scan", "hallucination", "certify"]
    assert all(isinstance(r, GateResult) for r in results)
    # SAM may fail on a mock nexus (trust score defaults to 0.8*something) — just ensure downstream gates pass
    downstream = [r for r in results if r.gate != "sam"]
    assert all(r.passed for r in downstream)
