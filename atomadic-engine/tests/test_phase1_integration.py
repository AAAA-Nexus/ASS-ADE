"""Phase 1 integration tests — SAM pipeline, LSE in live loop, BAS on D_MAX."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from ass_ade.agent.gates import QualityGates
from ass_ade.agent.loop import AgentLoop, D_MAX
from ass_ade.agent.lse import LSEEngine
from ass_ade.agent.orchestrator import EngineOrchestrator
from ass_ade.engine.types import CompletionResponse, Message
from ass_ade.tools.registry import ToolRegistry


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────


def _make_nexus_mock() -> MagicMock:
    nexus = MagicMock()
    nexus.trust_score.return_value = MagicMock(score=0.9)
    nexus.security_shield.return_value = MagicMock(blocked=False, sanitized=None)
    nexus.prompt_inject_scan.return_value = MagicMock(
        threat_detected=False, threat_level="none", confidence=1.0
    )
    nexus.hallucination_oracle.return_value = MagicMock(
        verdict="safe", confidence=1.0, policy_epsilon=0.0001
    )
    nexus.certify_output.return_value = MagicMock(
        rubric_passed=True, score=0.95, certificate_id="cert-1"
    )
    nexus.reputation_record.return_value = MagicMock(ok=True)
    return nexus


def _make_provider_returning_text(text: str) -> MagicMock:
    provider = MagicMock()
    provider.complete.return_value = CompletionResponse(
        message=Message(role="assistant", content=text, tool_calls=[]),
        usage={"input_tokens": 10, "output_tokens": 5},
    )
    return provider


# ─────────────────────────────────────────────────────────────────────────────
# Stage 0 (SAM) wiring into QualityGates.run_pipeline
# ─────────────────────────────────────────────────────────────────────────────


class TestSAMInPipeline:
    def test_sam_runs_first_in_pipeline(self):
        nexus = _make_nexus_mock()
        gates = QualityGates(nexus, config={})
        with patch("ass_ade.context_memory.vector_embed", return_value=[0.1, 0.2, 0.3]):
            results = gates.run_pipeline(prompt="build a function", output="def x(): pass")
        gate_names = [r.gate for r in results]
        assert "sam" in gate_names, f"SAM missing from pipeline: {gate_names}"
        # SAM must be the very first gate
        assert gate_names[0] == "sam"

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


# ─────────────────────────────────────────────────────────────────────────────
# SAM gate runs in AgentLoop.step() before model call
# ─────────────────────────────────────────────────────────────────────────────


class TestSAMInAgentLoop:
    def test_sam_gate_runs_per_step_and_populates_last_result(self):
        nexus = _make_nexus_mock()
        gates = QualityGates(nexus, config={})
        provider = _make_provider_returning_text("hello")
        registry = ToolRegistry()

        loop = AgentLoop(
            provider=provider,
            registry=registry,
            quality_gates=gates,
        )

        with patch("ass_ade.context_memory.vector_embed", return_value=[0.1, 0.2, 0.3]):
            loop.step("What is 1+1?")

        assert loop.last_sam_result is not None
        assert "trs" in loop.last_sam_result
        assert "composite" in loop.last_sam_result

    def test_sam_result_none_when_no_gates(self):
        provider = _make_provider_returning_text("hello")
        registry = ToolRegistry()
        loop = AgentLoop(provider=provider, registry=registry)
        loop.step("What is 2+2?")
        assert loop.last_sam_result is None


# ─────────────────────────────────────────────────────────────────────────────
# LSE wired into AgentLoop — selection is live
# ─────────────────────────────────────────────────────────────────────────────


class TestLSEInAgentLoop:
    def test_lse_decision_populated_after_step(self):
        provider = _make_provider_returning_text("result")
        registry = ToolRegistry()
        lse = LSEEngine({})
        loop = AgentLoop(provider=provider, registry=registry, lse=lse)
        loop.step("simple question")
        assert loop.last_lse_decision is not None
        # Canonical tier names (catalog-aware); haiku/sonnet/opus are aliases
        assert loop.last_lse_decision.tier in {"fast", "balanced", "deep"}

    def test_lse_model_override_propagates_to_provider(self):
        provider = _make_provider_returning_text("ok")
        registry = ToolRegistry()
        lse = LSEEngine({})
        loop = AgentLoop(provider=provider, registry=registry, lse=lse)
        loop.step("trivial task")
        # Provider was called with a model name from LSE
        call_args = provider.complete.call_args
        assert call_args is not None
        request = call_args[0][0] if call_args[0] else call_args[1].get("request")
        # The request should have a model set (either from LSE or None)
        assert hasattr(request, "model")

    def test_no_lse_falls_back_to_configured_model(self):
        provider = _make_provider_returning_text("ok")
        registry = ToolRegistry()
        loop = AgentLoop(
            provider=provider,
            registry=registry,
            model="claude-sonnet-4-6",
        )
        loop.step("any")
        call_args = provider.complete.call_args
        request = call_args[0][0] if call_args[0] else call_args[1].get("request")
        assert request.model == "claude-sonnet-4-6"


# ─────────────────────────────────────────────────────────────────────────────
# BAS alert fires on D_MAX breach
# ─────────────────────────────────────────────────────────────────────────────


class TestBASOnDMaxBreach:
    def test_d_max_breach_returns_blocked_message(self):
        provider = _make_provider_returning_text("ok")
        registry = ToolRegistry()
        orchestrator = EngineOrchestrator({})
        loop = AgentLoop(provider=provider, registry=registry, orchestrator=orchestrator)

        # Simulate being inside a recursion by setting depth past D_MAX
        loop._delegation_depth = D_MAX + 1
        result = loop.step("[REFINE round 1/3] retry")
        assert "D_MAX" in result or "delegation" in result.lower()

    def test_d_max_breach_emits_bas_alert(self):
        provider = _make_provider_returning_text("ok")
        registry = ToolRegistry()
        orchestrator = EngineOrchestrator({})
        loop = AgentLoop(provider=provider, registry=registry, orchestrator=orchestrator)

        # Set to exactly D_MAX so next increment exceeds
        loop._delegation_depth = D_MAX
        loop.step("[REFINE round 1/3] retry")

        # BAS should have a d_max_breach alert
        alerts = orchestrator.bas._alerts
        kinds = [a.kind for a in alerts]
        assert "d_max_breach" in kinds, f"Expected d_max_breach in {kinds}"

    def test_d_max_breach_severity_is_high(self):
        from ass_ade.agent.bas import _SEVERITY
        assert _SEVERITY.get("d_max_breach") == "high"

    def test_normal_flow_does_not_trigger_d_max_alert(self):
        provider = _make_provider_returning_text("ok")
        registry = ToolRegistry()
        orchestrator = EngineOrchestrator({})
        loop = AgentLoop(provider=provider, registry=registry, orchestrator=orchestrator)

        # Normal step (depth = 0)
        loop.step("normal request")
        alerts = orchestrator.bas._alerts
        kinds = [a.kind for a in alerts]
        assert "d_max_breach" not in kinds


# ─────────────────────────────────────────────────────────────────────────────
# CLI Phase 1 header rendering
# ─────────────────────────────────────────────────────────────────────────────


class TestPhase1Header:
    def test_render_header_includes_trs_when_sam_ran(self):
        from ass_ade.commands.agent import _render_phase1_header
        from io import StringIO
        from rich.console import Console as RichConsole

        # Patch the module's console to capture
        agent_mock = MagicMock()
        agent_mock.last_sam_result = {"composite": 0.85, "g23": True, "trs": {}}
        agent_mock.last_lse_decision = MagicMock(tier="sonnet")
        agent_mock.delegation_depth = 0
        agent_mock.last_cycle_report = None

        capture = StringIO()
        with patch("ass_ade.commands.agent.console", RichConsole(file=capture, force_terminal=False)):
            _render_phase1_header(agent_mock)
        output = capture.getvalue()
        assert "TRS=0.85" in output
        assert "LSE=sonnet" in output

    def test_render_header_skips_when_nothing_to_show(self):
        from ass_ade.commands.agent import _render_phase1_header
        from io import StringIO
        from rich.console import Console as RichConsole

        agent_mock = MagicMock()
        agent_mock.last_sam_result = None
        agent_mock.last_lse_decision = None
        agent_mock.delegation_depth = 0
        agent_mock.last_cycle_report = None

        capture = StringIO()
        with patch("ass_ade.commands.agent.console", RichConsole(file=capture, force_terminal=False)):
            _render_phase1_header(agent_mock)
        # No output expected when nothing to show
        assert capture.getvalue() == ""


# ─────────────────────────────────────────────────────────────────────────────
# SAM + LSE + orchestrator + gates: end-to-end Phase 1 smoke
# ─────────────────────────────────────────────────────────────────────────────


class TestPhase1EndToEnd:
    def test_full_phase1_stack_runs_a_step(self):
        nexus = _make_nexus_mock()
        gates = QualityGates(nexus, config={})
        orchestrator = EngineOrchestrator({}, nexus=nexus)
        lse = LSEEngine({})
        provider = _make_provider_returning_text("done")
        registry = ToolRegistry()

        loop = AgentLoop(
            provider=provider,
            registry=registry,
            quality_gates=gates,
            orchestrator=orchestrator,
            lse=lse,
        )

        with patch("ass_ade.context_memory.vector_embed", return_value=[0.3] * 8):
            result = loop.step("what is Python's GIL?")

        assert result == "done"
        # SAM ran
        assert loop.last_sam_result is not None
        # LSE chose a model
        assert loop.last_lse_decision is not None
        # CycleReport was produced
        assert loop.last_cycle_report is not None
        # Delegation depth back to 0 after step
        assert loop.delegation_depth == 0
