# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_persist_principles_calls_context_memory.py:7
# Component id: at.source.a1_at_functions.test_persist_principles_calls_context_memory
from __future__ import annotations

__version__ = "0.1.0"

def test_persist_principles_calls_context_memory(self):
    from ass_ade.agent.wisdom import WisdomEngine
    engine = WisdomEngine({})
    engine._principles = ["verify before acting", "halt on capability gap"]

    with patch("ass_ade.context_memory.store_vector_memory") as mock_store:
        count = engine.persist_principles()
    assert count == 2
