# Extracted from C:/!ass-ade/tests/test_engine_integration.py:56
# Component id: mo.source.ass_ade.testwisdomengine
from __future__ import annotations

__version__ = "0.1.0"

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
