# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testengineorchestratorphase15.py:23
# Component id: mo.source.ass_ade.test_cie_property_lazy_init
__version__ = "0.1.0"

    def test_cie_property_lazy_init(self):
        orch = self._make()
        cie = orch.cie
        assert cie is not None
