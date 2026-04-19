# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_lora_flywheel.py:7
# Component id: at.source.a1_at_functions.lora_flywheel
from __future__ import annotations

__version__ = "0.1.0"

def lora_flywheel(self):
    if self._lora_flywheel is None:
        from ass_ade.agent.lora_flywheel import LoRAFlywheel
        self._lora_flywheel = LoRAFlywheel(self._config, self._nexus)
    return self._lora_flywheel
