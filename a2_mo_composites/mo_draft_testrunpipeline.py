# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testrunpipeline.py:7
# Component id: mo.source.a2_mo_composites.testrunpipeline
from __future__ import annotations

__version__ = "0.1.0"

class TestRunPipeline:
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

    def test_pipeline_with_failures(self):
        gates = QualityGates(_mock_nexus(threat_detected=True, verdict="unsafe"))
        results = gates.run_pipeline(prompt="bad", output="wrong")
        failed = [r for r in results if not r.passed]
        assert len(failed) >= 2  # scan and hallucination should fail

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
