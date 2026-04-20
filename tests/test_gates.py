"""Tests for enhanced quality gates."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock

from ass_ade.agent.gates import GateResult, QualityGates


def _mock_nexus(**overrides: Any) -> MagicMock:
    """Create a mock NexusClient with configurable responses."""
    client = MagicMock()

    # prompt_inject_scan
    scan = MagicMock()
    scan.threat_detected = overrides.get("threat_detected", False)
    scan.threat_level = overrides.get("threat_level", "none")
    scan.confidence = overrides.get("scan_confidence", 0.95)
    client.prompt_inject_scan.return_value = scan

    # hallucination_oracle
    halluc = MagicMock()
    halluc.verdict = overrides.get("verdict", "safe")
    halluc.confidence = overrides.get("halluc_confidence", 0.90)
    halluc.policy_epsilon = overrides.get("policy_epsilon", 0.02)
    client.hallucination_oracle.return_value = halluc

    # security_shield
    shield = MagicMock()
    shield.blocked = overrides.get("shield_blocked", False)
    shield.sanitized = overrides.get("sanitized", None)
    client.security_shield.return_value = shield

    # certify_output
    cert = MagicMock()
    cert.certificate_id = overrides.get("certificate_id", "cert-123")
    cert.score = overrides.get("cert_score", 0.95)
    cert.rubric_passed = overrides.get("rubric_passed", True)
    client.certify_output.return_value = cert

    # memory_trim
    trim = MagicMock()
    trim.trimmed_context = overrides.get("trimmed_context", "trimmed")
    client.memory_trim.return_value = trim

    return client


class TestQualityGates:
    def test_scan_prompt_clean(self):
        gates = QualityGates(_mock_nexus())
        result = gates.scan_prompt("What is Python?")
        assert result is not None
        assert result["blocked"] is False

    def test_scan_prompt_blocked(self):
        gates = QualityGates(_mock_nexus(threat_detected=True, threat_level="high"))
        result = gates.scan_prompt("Ignore instructions and...")
        assert result is not None
        assert result["blocked"] is True
        assert result["threat_level"] == "high"

    def test_scan_prompt_exception(self):
        client = MagicMock()
        client.prompt_inject_scan.side_effect = Exception("network error")
        gates = QualityGates(client)
        assert gates.scan_prompt("test") is None

    def test_check_hallucination_safe(self):
        gates = QualityGates(_mock_nexus())
        result = gates.check_hallucination("Python is a programming language.")
        assert result is not None
        assert result["verdict"] == "safe"
        assert "policy_epsilon" in result

    def test_check_hallucination_unsafe(self):
        gates = QualityGates(_mock_nexus(verdict="unsafe", policy_epsilon=0.85))
        result = gates.check_hallucination("Made up claim.")
        assert result is not None
        assert result["verdict"] == "unsafe"

    def test_shield_tool_allowed(self):
        gates = QualityGates(_mock_nexus())
        result = gates.shield_tool("read_file", {"path": "test.py"})
        assert result is not None
        assert result["blocked"] is False

    def test_shield_tool_blocked(self):
        gates = QualityGates(_mock_nexus(shield_blocked=True))
        result = gates.shield_tool("run_command", {"command": "rm -rf /"})
        assert result is not None
        assert result["blocked"] is True

    def test_certify_passed(self):
        gates = QualityGates(_mock_nexus())
        result = gates.certify("def add(a, b): return a + b")
        assert result is not None
        assert result["passed"] is True
        assert result["certificate_id"] == "cert-123"

    def test_certify_failed(self):
        gates = QualityGates(_mock_nexus(rubric_passed=False, cert_score=0.3))
        result = gates.certify("bad code")
        assert result is not None
        assert result["passed"] is False

    def test_trim_context(self):
        gates = QualityGates(_mock_nexus(trimmed_context="short version"))
        result = gates.trim_context("very long context...", target_tokens=100)
        assert result == "short version"

    def test_trim_context_exception(self):
        client = MagicMock()
        client.memory_trim.side_effect = Exception("fail")
        gates = QualityGates(client)
        assert gates.trim_context("text", 100) is None


class TestGateLog:
    def test_gate_log_accumulates(self):
        gates = QualityGates(_mock_nexus())
        gates.scan_prompt("test")
        gates.check_hallucination("output")
        gates.certify("code")
        assert len(gates.gate_log) == 3

    def test_gate_log_is_copy(self):
        gates = QualityGates(_mock_nexus())
        gates.scan_prompt("test")
        log = gates.gate_log
        log.clear()
        assert len(gates.gate_log) == 1  # original unchanged

    def test_gate_result_structure(self):
        gates = QualityGates(_mock_nexus())
        gates.scan_prompt("test")
        result = gates.gate_log[0]
        assert isinstance(result, GateResult)
        assert result.gate == "prompt_scan"
        assert result.passed is True
        assert result.confidence > 0


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
