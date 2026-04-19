# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_batch_clears_pending_on_success.py:7
# Component id: at.source.a1_at_functions.test_batch_clears_pending_on_success
from __future__ import annotations

__version__ = "0.1.0"

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
