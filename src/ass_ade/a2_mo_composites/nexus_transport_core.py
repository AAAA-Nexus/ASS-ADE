"""Tier a2 — assimilated class 'NexusTransport'

Assimilated from: nexus.py:166-187
"""

from __future__ import annotations


# --- assimilated symbol ---
class NexusTransport(Protocol):
    """Structural type for the four §11 RPC hops.

    Production implementation delegates to the AAAA-Nexus MCP server
    at ``https://atomadic.tech/mcp`` via ``skills/aaaa-nexus-*``.
    Each method MUST raise :class:`NexusUnavailable` on transport
    failure (or the wrapper will re-raise after retries); each
    method MUST return the dict shape documented on the wrapper
    functions below.
    """

    def aegis_scan(self, envelope: Mapping[str, Any]) -> Mapping[str, Any]: ...

    def drift_check(self, envelope: Mapping[str, Any]) -> Mapping[str, Any]: ...

    def hallucination_check(
        self, outbound: Mapping[str, Any]
    ) -> Mapping[str, Any]: ...

    def trust_chain_sign(
        self, outbound: Mapping[str, Any], session: Mapping[str, Any] | None
    ) -> Mapping[str, Any]: ...

