# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_phase_engines.py:603
# Component id: mo.source.ass_ade.test_persist_principles_no_lora_on_low_conviction
__version__ = "0.1.0"

    def test_persist_principles_no_lora_on_low_conviction(self, tmp_path):
        from ass_ade.agent.wisdom import WisdomEngine
        from ass_ade.agent.lora_flywheel import LoRAFlywheel
        cfg = {
            "lora_flywheel": {
                "pending_file": str(tmp_path / "pending.jsonl"),
                "contributions_file": str(tmp_path / "contributions.jsonl"),
                "batch_interval": 50,
                "min_confidence": 0.5,
            }
        }
        engine = WisdomEngine({})
        engine._principles = ["p1", "p2", "p3"]
        engine._conviction = 0.3  # Below 0.7

        flywheel = LoRAFlywheel(cfg)
        with patch("ass_ade.context_memory.store_vector_memory"):
            engine.persist_principles(lora_flywheel=flywheel)
        # Low conviction → no LoRA contribution
        assert len(flywheel._pending) == 0
