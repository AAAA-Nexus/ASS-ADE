# Extracted from C:/!ass-ade/tests/test_phase_engines.py:571
# Component id: mo.source.ass_ade.testwisdompersistence
from __future__ import annotations

__version__ = "0.1.0"

class TestWisdomPersistence:
    def test_persist_principles_calls_context_memory(self):
        from ass_ade.agent.wisdom import WisdomEngine
        engine = WisdomEngine({})
        engine._principles = ["verify before acting", "halt on capability gap"]

        with patch("ass_ade.context_memory.store_vector_memory") as mock_store:
            count = engine.persist_principles()
        assert count == 2

    def test_persist_principles_triggers_lora_on_high_conviction(self, tmp_path):
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
        engine._principles = ["p1", "p2", "p3", "p4"]
        engine._conviction = 0.9  # High conviction

        flywheel = LoRAFlywheel(cfg)
        with patch("ass_ade.context_memory.store_vector_memory"):
            count = engine.persist_principles(lora_flywheel=flywheel)
        assert count == 4
        # Flywheel should have captured principles (≥3 and conviction ≥ 0.7)
        assert any(c.kind == "principle" for c in flywheel._pending)

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
