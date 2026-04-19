# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_batch_fail_keeps_pending.py:7
# Component id: at.source.a1_at_functions.test_batch_fail_keeps_pending
from __future__ import annotations

__version__ = "0.1.0"

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
