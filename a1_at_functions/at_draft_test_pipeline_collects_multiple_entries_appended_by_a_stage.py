# Extracted from C:/!ass-ade/tests/test_gates.py:163
# Component id: at.source.ass_ade.test_pipeline_collects_multiple_entries_appended_by_a_stage
from __future__ import annotations

__version__ = "0.1.0"

def test_pipeline_collects_multiple_entries_appended_by_a_stage(self):
    gates = QualityGates(_mock_nexus())

    original_scan = gates.scan_prompt

    def scan_with_extra(text: str):
        result = original_scan(text)
        gates._gate_log.append(GateResult(gate="scan_extra", passed=True, confidence=1.0))
        return result

    gates.scan_prompt = scan_with_extra  # type: ignore[method-assign]
    results = gates.run_pipeline(prompt="safe", output="safe")

    names = [r.gate for r in results]
    assert "prompt_scan" in names
    assert "scan_extra" in names
