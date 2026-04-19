# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_engine_integration.py:172
# Component id: mo.source.ass_ade.testbas
__version__ = "0.1.0"

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
