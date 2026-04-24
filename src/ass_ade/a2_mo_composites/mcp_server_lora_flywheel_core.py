"""Tier a2 — assimilated method 'MCPServer.lora_flywheel'

Assimilated from: server.py:568-590
"""

from __future__ import annotations


# --- assimilated symbol ---
def lora_flywheel(self) -> Any:
    if self._lora_flywheel is None:
        try:
            from ass_ade.agent.lora_flywheel import LoRAFlywheel
            from ass_ade.config import load_config
            from ass_ade.nexus.client import NexusClient

            settings = load_config()
            nexus = None
            if settings.profile in {"hybrid", "premium"} and settings.nexus_api_key:
                nexus = NexusClient(
                    base_url=settings.nexus_base_url,
                    timeout=settings.request_timeout_s,
                    api_key=settings.nexus_api_key,
                    agent_id=settings.agent_id,
                )
            self._lora_flywheel = LoRAFlywheel(
                nexus=nexus, session_id=f"mcp:{id(self)}"
            )
        except (ImportError, OSError, RuntimeError, TypeError, ValueError) as exc:
            _LOG.debug("LoRA flywheel init skipped: %s", exc)
            return None
    return self._lora_flywheel

