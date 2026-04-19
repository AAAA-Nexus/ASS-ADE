# Extracted from C:/!ass-ade/tests/test_phase_engines.py:630
# Component id: mo.source.ass_ade.testengineorchestratorphase15
from __future__ import annotations

__version__ = "0.1.0"

class TestEngineOrchestratorPhase15:
    def _make(self):
        from ass_ade.agent.orchestrator import EngineOrchestrator
        nexus = MagicMock()
        return EngineOrchestrator({}, nexus=nexus)

    def test_lse_property_lazy_init(self):
        orch = self._make()
        assert orch._lse is None
        lse = orch.lse
        assert lse is not None
        assert orch._lse is lse  # cached

    def test_tca_property_lazy_init(self):
        orch = self._make()
        tca = orch.tca
        assert tca is not None

    def test_cie_property_lazy_init(self):
        orch = self._make()
        cie = orch.cie
        assert cie is not None

    def test_lora_flywheel_property_lazy_init(self):
        orch = self._make()
        fly = orch.lora_flywheel
        assert fly is not None

    def test_check_conviction_gate_non_destructive_tool(self):
        orch = self._make()
        # Non-destructive tool: read_file should NOT be blocked
        blocked = orch.check_conviction_gate("read_file", {})
        assert blocked is False

    def test_check_conviction_gate_destructive_no_audits_passes(self):
        orch = self._make()
        # write_file with 0 audits → should not block (no audit history yet)
        blocked = orch.check_conviction_gate("write_file", {})
        assert blocked is False

    def test_engine_report_includes_new_engines_after_init(self):
        orch = self._make()
        # Touch the new engines to init them
        _ = orch.lse
        _ = orch.tca
        _ = orch.cie
        _ = orch.lora_flywheel
        rep = orch.engine_report()
        assert "lse" in rep
        assert "tca" in rep
        assert "cie" in rep
        assert "lora_flywheel" in rep

    def test_wisdom_ema_initialized(self):
        orch = self._make()
        assert orch._wisdom_ema == 0.5

    def test_consecutive_low_wisdom_starts_zero(self):
        orch = self._make()
        assert orch._consecutive_low_wisdom == 0

    def test_cycle_report_has_new_fields(self):
        from ass_ade.agent.orchestrator import CycleReport
        report = CycleReport(alerts=[])
        assert hasattr(report, "wisdom_ema")
        assert hasattr(report, "tca_stale_files")
        assert hasattr(report, "cie_passes")
        assert hasattr(report, "lora_pending")
        assert hasattr(report, "autopoietic_triggered")
