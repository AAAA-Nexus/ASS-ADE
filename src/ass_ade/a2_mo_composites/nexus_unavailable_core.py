"""Tier a2 — assimilated class 'NexusUnavailable'

Assimilated from: nexus.py:73-80
"""

from __future__ import annotations


# --- assimilated symbol ---
class NexusUnavailable(NexusError):
    """Transport exhausted its retry budget without a successful response.

    Raised after three failed attempts to reach the Nexus MCP. Fail-
    closed per ``_PROTOCOL.md §11.5`` — callers MUST NOT degrade to
    local-only reasoning. Recovery is to surface the failure to the
    operator; the parent agent refreshes the session and retries.
    """

