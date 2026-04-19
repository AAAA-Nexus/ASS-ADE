# Extracted from C:/!ass-ade/tests/test_phase_engines.py:444
# Component id: mo.source.ass_ade.test_pending_persists_across_instances
from __future__ import annotations

__version__ = "0.1.0"

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
