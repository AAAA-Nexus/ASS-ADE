# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testqualitygates.py:5
# Component id: mo.source.ass_ade.testqualitygates
__version__ = "0.1.0"

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
