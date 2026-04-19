# Extracted from C:/!ass-ade/tests/test_engine_integration.py:284
# Component id: mo.source.ass_ade.testengineorchestrator
from __future__ import annotations

__version__ = "0.1.0"

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
