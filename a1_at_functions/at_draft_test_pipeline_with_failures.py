# Extracted from C:/!ass-ade/tests/test_gates.py:157
# Component id: at.source.ass_ade.test_pipeline_with_failures
from __future__ import annotations

__version__ = "0.1.0"

def test_pipeline_with_failures(self):
    gates = QualityGates(_mock_nexus(threat_detected=True, verdict="unsafe"))
    results = gates.run_pipeline(prompt="bad", output="wrong")
    failed = [r for r in results if not r.passed]
    assert len(failed) >= 2  # scan and hallucination should fail
