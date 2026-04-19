# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_pipeline_with_failures.py:7
# Component id: at.source.a1_at_functions.test_pipeline_with_failures
from __future__ import annotations

__version__ = "0.1.0"

def test_pipeline_with_failures(self):
    gates = QualityGates(_mock_nexus(threat_detected=True, verdict="unsafe"))
    results = gates.run_pipeline(prompt="bad", output="wrong")
    failed = [r for r in results if not r.passed]
    assert len(failed) >= 2  # scan and hallucination should fail
