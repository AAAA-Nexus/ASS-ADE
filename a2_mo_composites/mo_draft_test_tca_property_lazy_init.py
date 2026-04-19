# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testengineorchestratorphase15.py:18
# Component id: mo.source.ass_ade.test_tca_property_lazy_init
__version__ = "0.1.0"

    def test_tca_property_lazy_init(self):
        orch = self._make()
        tca = orch.tca
        assert tca is not None
