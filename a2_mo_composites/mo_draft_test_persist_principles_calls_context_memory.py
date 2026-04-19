# Extracted from C:/!ass-ade/tests/test_phase_engines.py:572
# Component id: mo.source.ass_ade.test_persist_principles_calls_context_memory
from __future__ import annotations

__version__ = "0.1.0"

def test_persist_principles_calls_context_memory(self):
    from ass_ade.agent.wisdom import WisdomEngine
    engine = WisdomEngine({})
    engine._principles = ["verify before acting", "halt on capability gap"]

    with patch("ass_ade.context_memory.store_vector_memory") as mock_store:
        count = engine.persist_principles()
    assert count == 2
