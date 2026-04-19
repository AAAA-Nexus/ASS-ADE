# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_disabled_flywheel_rejects_captures.py:7
# Component id: at.source.a1_at_functions.test_disabled_flywheel_rejects_captures
from __future__ import annotations

__version__ = "0.1.0"

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
