# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testengineorchestratorphase15.py:11
# Component id: mo.source.ass_ade.test_lse_property_lazy_init
__version__ = "0.1.0"

    def test_lse_property_lazy_init(self):
        orch = self._make()
        assert orch._lse is None
        lse = orch.lse
        assert lse is not None
        assert orch._lse is lse  # cached
