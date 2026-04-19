# Extracted from C:/!ass-ade/tests/test_phase_engines.py:407
# Component id: mo.source.ass_ade.testloraflywheel
from __future__ import annotations

__version__ = "0.1.0"

class TestLoRAFlywheel:
    def _make(self, tmp_path):
        from ass_ade.agent.lora_flywheel import LoRAFlywheel
        cfg = {
            "lora_flywheel": {
                "pending_file": str(tmp_path / "pending.jsonl"),
                "contributions_file": str(tmp_path / "contributions.jsonl"),
                "batch_interval": 5,  # Short for tests
                "min_confidence": 0.5,
            }
        }
        return LoRAFlywheel(cfg, session_id="test-session")

    def test_capture_fix_adds_to_pending(self, tmp_path):
        fly = self._make(tmp_path)
        cid = fly.capture_fix("old code", "new code")
        assert cid != ""
        assert len(fly._pending) == 1
        assert fly._pending[0].kind == "fix"

    def test_capture_principle_adds_to_pending(self, tmp_path):
        fly = self._make(tmp_path)
        cid = fly.capture_principle("always verify before acting", confidence=0.9)
        assert cid != ""
        assert fly._pending[0].kind == "principle"

    def test_low_confidence_principle_skipped(self, tmp_path):
        fly = self._make(tmp_path)
        cid = fly.capture_principle("weak idea", confidence=0.1)
        assert cid == ""
        assert len(fly._pending) == 0

    def test_capture_rejection_adds_negative(self, tmp_path):
        fly = self._make(tmp_path)
        fly.capture_rejection("bad code", "A03_injection_eval")
        assert fly._pending[0].kind == "rejection"

    def test_pending_persists_across_instances(self, tmp_path):
        from ass_ade.agent.lora_flywheel import LoRAFlywheel
        cfg = {
            "lora_flywheel": {
                "pending_file": str(tmp_path / "pending.jsonl"),
                "contributions_file": str(tmp_path / "contributions.jsonl"),
                "batch_interval": 50,
                "min_confidence": 0.5,
            }
        }
        f1 = LoRAFlywheel(cfg, session_id="s1")
        f1.capture_fix("a", "b")
        f2 = LoRAFlywheel(cfg, session_id="s1")
        assert len(f2._pending) == 1

    def test_batch_clears_pending_on_success(self, tmp_path):
        nexus = MagicMock()
        nexus.lora_contribute.return_value = MagicMock(contribution_id="cid-123")
        from ass_ade.agent.lora_flywheel import LoRAFlywheel
        cfg = {
            "lora_flywheel": {
                "pending_file": str(tmp_path / "pending.jsonl"),
                "contributions_file": str(tmp_path / "contributions.jsonl"),
                "batch_interval": 50,
                "min_confidence": 0.5,
            }
        }
        fly = LoRAFlywheel(cfg, nexus=nexus, session_id="s1")
        fly.capture_fix("x", "y")
        result = fly.contribute_batch()
        assert result.submitted == 1
        assert len(fly._pending) == 0

    def test_batch_uses_configured_trust_floor_threshold(self, tmp_path):
        nexus = MagicMock()
        nexus.lora_contribute.return_value = {"accepted": 1, "rejected": 0}
        from ass_ade.agent.lora_flywheel import LoRAFlywheel
        cfg = {
            "lora_flywheel": {
                "pending_file": str(tmp_path / "pending.jsonl"),
                "contributions_file": str(tmp_path / "contributions.jsonl"),
                "batch_interval": 50,
                "min_confidence": 0.5,
                "trust_floor_threshold": 0.17,
            }
        }
        fly = LoRAFlywheel(cfg, nexus=nexus, session_id="s1")
        fly.capture_fix("old code with extra checks", "new code")
        result = fly.contribute_batch()
        assert result.submitted == 1
        assert nexus.lora_contribute.call_args.kwargs["trust_floor_threshold"] == 0.17

    def test_batch_fail_keeps_pending(self, tmp_path):
        nexus = MagicMock()
        nexus.lora_contribute.side_effect = RuntimeError("network error")
        nexus.lora_capture_fix.side_effect = RuntimeError("also broken")
        from ass_ade.agent.lora_flywheel import LoRAFlywheel
        cfg = {
            "lora_flywheel": {
                "pending_file": str(tmp_path / "pending.jsonl"),
                "contributions_file": str(tmp_path / "contributions.jsonl"),
                "batch_interval": 50,
                "min_confidence": 0.5,
            }
        }
        fly = LoRAFlywheel(cfg, nexus=nexus, session_id="s1")
        fly.capture_fix("x", "y")
        result = fly.contribute_batch()
        assert result.submitted == 0
        assert result.error is not None
        assert len(fly._pending) == 1  # still there

    def test_tick_triggers_batch_at_interval(self, tmp_path):
        nexus = MagicMock()
        nexus.lora_contribute.return_value = MagicMock(contribution_id="cid-1")
        from ass_ade.agent.lora_flywheel import LoRAFlywheel
        cfg = {
            "lora_flywheel": {
                "pending_file": str(tmp_path / "pending.jsonl"),
                "contributions_file": str(tmp_path / "contributions.jsonl"),
                "batch_interval": 3,
                "min_confidence": 0.5,
            }
        }
        fly = LoRAFlywheel(cfg, nexus=nexus, session_id="s1")
        fly.capture_fix("a", "b")
        # Tick 3 times to trigger batch
        for _ in range(2):
            assert fly.tick() is None
        result = fly.tick()
        assert result is not None
        assert result.submitted == 1

    def test_status_structure(self, tmp_path):
        fly = self._make(tmp_path)
        status = fly.status()
        assert hasattr(status, "adapter_version")
        assert hasattr(status, "contribution_count")
        assert hasattr(status, "ratchet_epoch")
        assert hasattr(status, "pending_count")

    def test_rg_loop_constant_is_47(self):
        from ass_ade.agent.lora_flywheel import RG_LOOP
        assert RG_LOOP == 47

    def test_disabled_flywheel_rejects_captures(self, tmp_path):
        from ass_ade.agent.lora_flywheel import LoRAFlywheel
        cfg = {
            "lora_flywheel": {
                "pending_file": str(tmp_path / "pending.jsonl"),
                "contributions_file": str(tmp_path / "contributions.jsonl"),
                "enabled": False,
                "batch_interval": 5,
                "min_confidence": 0.5,
            }
        }
        fly = LoRAFlywheel(cfg)
        cid = fly.capture_fix("old", "new")
        assert cid == ""
        assert len(fly._pending) == 0
