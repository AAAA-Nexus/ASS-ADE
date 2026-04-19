# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_batch_uses_configured_trust_floor_threshold.py:7
# Component id: at.source.a1_at_functions.test_batch_uses_configured_trust_floor_threshold
from __future__ import annotations

__version__ = "0.1.0"

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
