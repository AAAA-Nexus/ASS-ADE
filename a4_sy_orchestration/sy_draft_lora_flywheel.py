# Extracted from C:/!ass-ade/src/ass_ade/agent/orchestrator.py:285
# Component id: sy.source.ass_ade.lora_flywheel
from __future__ import annotations

__version__ = "0.1.0"

def lora_flywheel(self):
    if self._lora_flywheel is None:
        from ass_ade.agent.lora_flywheel import LoRAFlywheel
        self._lora_flywheel = LoRAFlywheel(self._config, self._nexus)
    return self._lora_flywheel
