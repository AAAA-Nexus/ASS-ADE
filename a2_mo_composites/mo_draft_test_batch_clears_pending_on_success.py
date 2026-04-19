# Extracted from C:/!ass-ade/tests/test_phase_engines.py:459
# Component id: mo.source.ass_ade.test_batch_clears_pending_on_success
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
