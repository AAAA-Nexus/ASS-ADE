# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_phase_engines.py:549
# Component id: mo.source.ass_ade.test_disabled_flywheel_rejects_captures
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
