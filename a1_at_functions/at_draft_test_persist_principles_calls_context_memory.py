# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testwisdompersistence.py:6
# Component id: at.source.ass_ade.test_persist_principles_calls_context_memory
__version__ = "0.1.0"

    def test_persist_principles_calls_context_memory(self):
        from ass_ade.agent.wisdom import WisdomEngine
        engine = WisdomEngine({})
        engine._principles = ["verify before acting", "halt on capability gap"]

        with patch("ass_ade.context_memory.store_vector_memory") as mock_store:
            count = engine.persist_principles()
        assert count == 2
