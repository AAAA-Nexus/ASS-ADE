"""Integration tests for v18 engine orchestration.

Covers:
- BAS: 8 alert types, persistence, cooldown, subscribers, monitor_all, flush
- WisdomEngine: 50 questions, conviction, gate_action, distill_principles, warnings
- AuditQuestions: 50 distinct texts, correct groups
- EngineOrchestrator: lifecycle hooks, lazy init, CycleReport
- AgentLoop: orchestrator wiring, last_cycle_report
- QualityGates: config parameter, _v18_config set correctly
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from ass_ade.agent.audit_questions import AUDIT_QUESTIONS
from ass_ade.agent.bas import BAS, Alert
from ass_ade.agent.gates import QualityGates
from ass_ade.agent.orchestrator import CycleReport, EngineOrchestrator
from ass_ade.agent.wisdom import AuditReport, WisdomEngine


# ── AuditQuestions ────────────────────────────────────────────────────────────

class TestAuditQuestions:
    def test_count_is_50(self) -> None:
        assert len(AUDIT_QUESTIONS) == 50

    def test_all_texts_unique(self) -> None:
        texts = [q["text"] for q in AUDIT_QUESTIONS]
        assert len(set(texts)) == 50, "All 50 audit questions must have distinct text"

    def test_ids_are_1_to_50(self) -> None:
        ids = sorted(q["id"] for q in AUDIT_QUESTIONS)
        assert ids == list(range(1, 51))

    def test_five_groups_of_ten(self) -> None:
        from collections import Counter
        groups = Counter(q["group"] for q in AUDIT_QUESTIONS)
        assert set(groups.keys()) == {"foundational", "operational", "autonomous", "meta_cognition", "hyperagent"}
        assert all(v == 10 for v in groups.values())

    def test_all_have_required_keys(self) -> None:
        for q in AUDIT_QUESTIONS:
            assert "id" in q and "group" in q and "text" in q
            assert isinstance(q["text"], str) and q["text"]


# ── WisdomEngine ──────────────────────────────────────────────────────────────

class TestWisdomEngine:
    def test_empty_cycle_state_fails_all(self) -> None:
        w = WisdomEngine({})
        report = w.run_audit({})
        assert report.failed == 50
        assert report.passed == 0
        assert report.score == 0.0

    def test_full_signal_state_passes_groups(self) -> None:
        w = WisdomEngine({})
        cycle_state = {
            "recon_done": True,
            "complexity_scored": True,
            "tier": "hybrid",
            "memory_consulted": True,
            "lifr_queried": True,
            "trace_captured": True,
            "hallucination_checked": True,
            "certified": True,
            "map_terrain_done": True,
            "atlas_used": True,
            "tdmi_computed": True,
            "budget_ok": True,
            "tool_calls": ["read_file"],
        }
        report = w.run_audit(cycle_state)
        assert report.passed > 0
        assert report.score > 0.0

    def test_explicit_qN_override(self) -> None:
        w = WisdomEngine({})
        report = w.run_audit({"q1": True, "q2": False, "q3": True})
        # q1 and q3 explicitly True, q2 False
        assert report.passed >= 2
        found_q2_fail = any(f["id"] == 2 for f in report.failures)
        assert found_q2_fail

    def test_conviction_ema(self) -> None:
        w = WisdomEngine({})
        r1 = w.run_audit({})  # score 0, conviction = 0.5*0.5 + 0.5*0 = 0.25
        assert abs(w.conviction - 0.25) < 0.01
        assert not w.is_confident  # well below 0.85

    def test_is_confident_true(self) -> None:
        w = WisdomEngine({"sde": {"conviction_required": 0.1}})
        # full state
        full = {f"q{i}": True for i in range(1, 51)}
        w.run_audit(full)
        assert w.is_confident

    def test_low_conviction_warning_fires_on_second_audit(self) -> None:
        w = WisdomEngine({})
        r1 = w.run_audit({})   # first audit — no warning even if low
        assert not any("low_conviction" in warn for warn in r1.warnings)
        r2 = w.run_audit({})   # second with still-low score — warning fires
        assert any("low_conviction" in warn for warn in r2.warnings)

    def test_gate_action_blocks_below_conviction(self) -> None:
        w = WisdomEngine({})
        w.run_audit({})  # conviction → 0.25
        ok, reason = w.gate_action("deploy_to_prod", {})
        assert not ok
        assert "conviction" in reason

    def test_gate_action_allows_above_conviction(self) -> None:
        w = WisdomEngine({"sde": {"conviction_required": 0.0}})
        ok, reason = w.gate_action("read_file", {})
        assert ok
        assert reason == "conviction_met"

    def test_distill_principles_from_failures(self) -> None:
        w = WisdomEngine({})
        report = w.run_audit({})  # all failed
        principles = w.distill_principles(report)
        assert isinstance(principles, list)
        assert len(principles) >= 1
        assert all(isinstance(p, str) and p for p in principles)

    def test_distill_principles_fallback_defaults(self) -> None:
        w = WisdomEngine({})
        principles = w.distill_principles(None)
        assert len(principles) >= 3

    def test_update_principles_deduplicates(self) -> None:
        w = WisdomEngine({})
        w.update_principles(["prefer reuse over regeneration"])
        w.update_principles(["prefer reuse over regeneration", "new principle"])
        assert w._principles.count("prefer reuse over regeneration") == 1
        assert "new principle" in w._principles

    def test_audit_report_has_warnings_field(self) -> None:
        w = WisdomEngine({})
        report = w.run_audit({})
        assert hasattr(report, "warnings")
        assert isinstance(report.warnings, list)

    def test_audit_report_has_principles_field(self) -> None:
        w = WisdomEngine({})
        report = w.run_audit({})
        assert hasattr(report, "principles")
        assert isinstance(report.principles, list)

    def test_run_returns_dict(self) -> None:
        w = WisdomEngine({})
        result = w.run({"cycle_state": {}})
        assert "passed" in result and "failed" in result and "score" in result

    def test_report_returns_engine_info(self) -> None:
        w = WisdomEngine({})
        r = w.report()
        assert r["engine"] == "wisdom"
        assert "conviction" in r and "conviction_required" in r


# ── BAS ───────────────────────────────────────────────────────────────────────

class TestBAS:
    def test_monitor_synergy_alert(self) -> None:
        b = BAS({"synergy": {"threshold": 0.5}})
        a = b.monitor({"synergy": 0.8, "novelty": 0.0, "gvu_delta": 0.0})
        assert a is not None
        assert a.kind == "emergent_synergy"
        assert a.severity == "high"

    def test_monitor_returns_none_below_threshold(self) -> None:
        b = BAS({})
        a = b.monitor({"synergy": 0.1, "novelty": 0.1, "gvu_delta": 0.0})
        assert a is None

    def test_monitor_all_fires_multiple_alerts(self) -> None:
        b = BAS({})
        alerts = b.monitor_all({
            "synergy": 0.9,
            "novelty": 0.9,
            "trust_score": 0.1,
            "budget_pct": 0.95,
            "gvu_delta": 0.0,
        })
        kinds = {a.kind for a in alerts}
        assert "emergent_synergy" in kinds
        assert "trust_violation" in kinds
        assert "budget_exhaustion" in kinds

    def test_capability_gap_alert(self) -> None:
        b = BAS({})
        alerts = b.monitor_all({"missing_capabilities": ["llm", "search"]})
        kinds = {a.kind for a in alerts}
        assert "capability_gap" in kinds

    def test_quality_regression_alert(self) -> None:
        b = BAS({})
        alerts = b.monitor_all({"score_delta": -0.5})
        kinds = {a.kind for a in alerts}
        assert "quality_regression" in kinds

    def test_loop_detected_alert(self) -> None:
        b = BAS({})
        alerts = b.monitor_all({"tool_repeat_count": 5})
        kinds = {a.kind for a in alerts}
        assert "loop_detected" in kinds

    def test_subscriber_called_on_alert(self) -> None:
        b = BAS({})
        received: list[Alert] = []
        b.subscribe(lambda a: received.append(a))
        b.monitor_all({"synergy": 0.9})
        assert len(received) >= 1
        assert received[0].kind == "emergent_synergy"

    def test_subscriber_exception_does_not_propagate(self) -> None:
        b = BAS({})
        b.subscribe(lambda a: (_ for _ in ()).throw(RuntimeError("boom")))
        # Should not raise
        b.monitor_all({"synergy": 0.9})

    def test_flush_alerts_drains_buffer(self) -> None:
        b = BAS({})
        b.monitor_all({"synergy": 0.9, "trust_score": 0.1})
        flushed = b.flush_alerts()
        assert len(flushed) >= 1
        # second flush is empty
        assert b.flush_alerts() == []

    def test_cooldown_prevents_duplicate_alerts(self) -> None:
        b = BAS({"bas_cooldown_s": 3600.0})  # 1-hour cooldown
        a1 = b.alert("gvu_jump", {"gvu_delta": 0.5})
        a2 = b.alert("gvu_jump", {"gvu_delta": 0.6})
        # second alert on cooldown
        assert a2.cooldown_skipped

    def test_persistence_writes_jsonl(self, tmp_path: Path) -> None:
        state_file = tmp_path / "alerts.jsonl"
        b = BAS({"bas_state_path": str(state_file)})
        b.alert("novelty_spike", {"novelty": 0.8})
        assert state_file.exists()
        lines = [json.loads(line) for line in state_file.read_text().strip().splitlines()]
        assert lines[0]["kind"] == "novelty_spike"

    def test_persistence_io_error_does_not_crash(self, tmp_path: Path) -> None:
        # Point to a directory path (not writable as file)
        b = BAS({"bas_state_path": str(tmp_path)})
        b.alert("novelty_spike", {"novelty": 0.8})  # should not raise

    def test_alert_severity_mapping(self) -> None:
        b = BAS({})
        high_kinds = ["emergent_synergy", "gvu_jump", "trust_violation", "budget_exhaustion"]
        for kind in high_kinds:
            a = Alert(kind=kind, severity="", payload={}, ts="")
            b_alert = b.alert(kind, {})
            assert b_alert.severity == "high", f"{kind} should be high severity"

    def test_report_structure(self) -> None:
        b = BAS({})
        r = b.report()
        assert r["engine"] == "bas"
        assert "alerts_total" in r
        assert "alerts_session" in r
        assert "unflushed" in r
        assert "cooldown_s" in r

    def test_run_returns_dict(self) -> None:
        b = BAS({})
        result = b.run({"metrics": {"synergy": 0.9}})
        assert "alert" in result


# ── EngineOrchestrator ────────────────────────────────────────────────────────

class TestEngineOrchestrator:
    def test_lazy_init_atlas(self) -> None:
        o = EngineOrchestrator({})
        assert o._atlas is None
        _ = o.atlas
        assert o._atlas is not None

    def test_on_step_start_returns_dict(self) -> None:
        o = EngineOrchestrator({})
        result = o.on_step_start("implement auth system")
        assert isinstance(result, dict)
        assert "atlas_subtasks" in result
        assert "puppeteer_next" in result

    def test_on_step_start_atlas_complexity(self) -> None:
        o = EngineOrchestrator({})
        result = o.on_step_start("a" * 2000)  # long = high complexity
        assert result["atlas_complexity"] > 1.0

    def test_on_tool_event_tracks_repeat(self) -> None:
        o = EngineOrchestrator({})
        o.on_step_start("task")
        for _ in range(4):
            o.on_tool_event("read_file", {"path": "x"}, "ok")
        # After 4 repeats, loop_detected should fire
        # Check _step_tool_counts
        assert o._step_tool_counts.get("read_file", 0) == 4

    def test_on_step_end_returns_cycle_report(self) -> None:
        o = EngineOrchestrator({})
        o.on_step_start("do something")
        report = o.on_step_end("done", {"recon_done": True, "tool_calls": ["read_file"]})
        assert isinstance(report, CycleReport)
        assert isinstance(report.wisdom_score, float)
        assert isinstance(report.conviction, float)
        assert isinstance(report.alerts, list)
        assert isinstance(report.principles, list)
        assert isinstance(report.engine_reports, dict)

    def test_on_step_end_wisdom_scores(self) -> None:
        o = EngineOrchestrator({})
        o.on_step_start("task")
        report = o.on_step_end("response", {
            "recon_done": True,
            "atlas_used": True,
            "lifr_queried": True,
            "memory_consulted": True,
            "budget_ok": True,
            "tool_calls": ["read_file"],
        })
        assert report.wisdom_score > 0.0
        assert report.wisdom_passed > 0

    def test_on_step_end_gvu_updated(self) -> None:
        o = EngineOrchestrator({})
        o.on_step_start("task")
        report = o.on_step_end("response", {})
        assert report.gvu_coefficient > 0.0

    def test_on_step_end_edee_traces(self) -> None:
        o = EngineOrchestrator({})
        o.on_step_start("task")
        report = o.on_step_end("response", {})
        # EDEE should be initialized and have captured a trace
        assert o._edee is not None
        assert o.edee._traces >= 1

    def test_step_metrics_reset_on_start(self) -> None:
        o = EngineOrchestrator({})
        o.on_step_start("first task")
        o.on_tool_event("read_file", {}, "")
        assert o._step_tool_counts.get("read_file", 0) == 1
        # Second step start should reset
        o.on_step_start("second task")
        assert o._step_tool_counts == {}

    def test_engine_report_aggregates_initialized_engines(self) -> None:
        o = EngineOrchestrator({})
        _ = o.atlas  # initialize atlas
        _ = o.bas    # initialize bas
        reports = o.engine_report()
        assert "atlas" in reports
        assert "bas" in reports

    def test_fail_open_on_engine_error(self) -> None:
        o = EngineOrchestrator({})
        # Corrupt the atlas to simulate failure
        o._atlas = MagicMock()
        o._atlas.decompose.side_effect = RuntimeError("engine crashed")
        o._atlas.complexity_score.side_effect = RuntimeError("engine crashed")
        # on_step_start should not raise
        result = o.on_step_start("task")
        assert isinstance(result, dict)

    def test_bas_subscriber_via_orchestrator(self) -> None:
        o = EngineOrchestrator({})
        received: list = []
        o.bas.subscribe(lambda a: received.append(a.kind))
        o.on_step_start("task")
        o.on_step_end("response", {"trust_score": 0.05, "budget_pct": 0.99})
        assert len(received) >= 1


# ── QualityGates config fix ───────────────────────────────────────────────────

class TestQualityGatesConfig:
    def test_default_config_is_empty_dict(self) -> None:
        mock_client = MagicMock()
        gates = QualityGates(mock_client)
        assert gates._v18_config == {}

    def test_config_passed_through(self) -> None:
        mock_client = MagicMock()
        config = {"alphaverus": {"beam_width": 8}, "dgm_h": {"simulation_cycles": 20}}
        gates = QualityGates(mock_client, config=config)
        assert gates._v18_config == config

    def test_hooks_receive_config(self) -> None:
        mock_client = MagicMock()
        mock_client.certify_output_verify.return_value = MagicMock(rubric_passed=True)
        config = {"alphaverus": {"beam_width": 2}}
        gates = QualityGates(mock_client, config=config)
        # hook_alphaverus_refine uses self._v18_config — verify it's the right dict
        with patch("ass_ade.agent.alphaverus.AlphaVerus") as MockAV:
            instance = MockAV.return_value
            instance.tree_search.return_value = MagicMock(code="x=1", verified=True, score=0.9)
            result = gates.hook_alphaverus_refine("x = 1", "x == 1")
            # AlphaVerus was instantiated with our config
            MockAV.assert_called_once_with(config, mock_client)


# ── AgentLoop + Orchestrator wiring ──────────────────────────────────────────

class TestAgentLoopOrchestrator:
    def _make_loop(self, orchestrator=None):
        from ass_ade.agent.loop import AgentLoop
        from ass_ade.engine.provider import ModelProvider
        from ass_ade.engine.types import CompletionResponse, Message
        from ass_ade.tools.registry import default_registry

        mock_provider = MagicMock(spec=ModelProvider)
        mock_provider.complete.return_value = CompletionResponse(
            message=Message(role="assistant", content="Done.", tool_calls=[]),
            usage={"input_tokens": 10, "output_tokens": 5},
        )
        return AgentLoop(
            provider=mock_provider,
            registry=default_registry(),
            orchestrator=orchestrator,
        )

    def test_loop_accepts_orchestrator_param(self) -> None:
        o = EngineOrchestrator({})
        loop = self._make_loop(orchestrator=o)
        assert loop._orchestrator is o

    def test_last_cycle_report_none_before_step(self) -> None:
        loop = self._make_loop()
        assert loop.last_cycle_report is None

    def test_last_cycle_report_set_after_step(self) -> None:
        o = EngineOrchestrator({})
        loop = self._make_loop(orchestrator=o)
        loop.step("Write hello world")
        assert loop.last_cycle_report is not None
        assert isinstance(loop.last_cycle_report, CycleReport)

    def test_step_without_orchestrator_still_works(self) -> None:
        loop = self._make_loop(orchestrator=None)
        result = loop.step("Hello")
        assert isinstance(result, str)

    def test_orchestrator_on_step_start_called(self) -> None:
        o = MagicMock(spec=EngineOrchestrator)
        o.on_step_start.return_value = {}
        o.on_tool_event.return_value = []
        o.on_step_end.return_value = CycleReport(alerts=[])

        loop = self._make_loop(orchestrator=o)
        loop.step("Do something")
        o.on_step_start.assert_called_once()

    def test_orchestrator_on_step_end_called(self) -> None:
        o = MagicMock(spec=EngineOrchestrator)
        o.on_step_start.return_value = {}
        o.on_tool_event.return_value = []
        o.on_step_end.return_value = CycleReport(alerts=[])

        loop = self._make_loop(orchestrator=o)
        loop.step("Do something")
        o.on_step_end.assert_called_once()

    def test_orchestrator_error_does_not_block_loop(self) -> None:
        o = MagicMock(spec=EngineOrchestrator)
        o.on_step_start.side_effect = RuntimeError("engine down")
        o.on_tool_event.side_effect = RuntimeError("engine down")
        o.on_step_end.side_effect = RuntimeError("engine down")

        loop = self._make_loop(orchestrator=o)
        # Should not raise — fail-open design
        result = loop.step("Do something")
        assert isinstance(result, str)
