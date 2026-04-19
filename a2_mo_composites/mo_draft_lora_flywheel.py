# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_engineorchestrator.py:209
# Component id: mo.source.ass_ade.lora_flywheel
__version__ = "0.1.0"

    def lora_flywheel(self):
        if self._lora_flywheel is None:
            from ass_ade.agent.lora_flywheel import LoRAFlywheel
            self._lora_flywheel = LoRAFlywheel(self._config, self._nexus)
        return self._lora_flywheel
