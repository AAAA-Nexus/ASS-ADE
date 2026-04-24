"""Tier a2 — assimilated method 'MCPServer._get_nexus_client'

Assimilated from: server.py:1043-1058
"""

from __future__ import annotations


# --- assimilated symbol ---
def _get_nexus_client(self) -> Any:
    """Create a NexusClient from config, or raise if unavailable."""
    from ass_ade.config import load_config

    cfg = load_config()
    if cfg.profile == "local":
        raise RuntimeError(
            "Workflow tools require hybrid or premium profile (current: local)"
        )
    from ass_ade.nexus.client import NexusClient

    return NexusClient(
        base_url=cfg.nexus_base_url or "https://atomadic.tech",
        timeout=cfg.request_timeout_s,
        api_key=cfg.nexus_api_key,
    )

