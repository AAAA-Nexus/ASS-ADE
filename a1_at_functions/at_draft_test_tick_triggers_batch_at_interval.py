# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_tick_triggers_batch_at_interval.py:7
# Component id: at.source.a1_at_functions.test_tick_triggers_batch_at_interval
from __future__ import annotations

__version__ = "0.1.0"

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
