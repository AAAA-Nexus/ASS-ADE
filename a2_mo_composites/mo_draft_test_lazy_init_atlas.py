# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_engine_integration.py:285
# Component id: mo.source.ass_ade.test_lazy_init_atlas
__version__ = "0.1.0"

    def test_lazy_init_atlas(self) -> None:
        o = EngineOrchestrator({})
        assert o._atlas is None
        _ = o.atlas
        assert o._atlas is not None
