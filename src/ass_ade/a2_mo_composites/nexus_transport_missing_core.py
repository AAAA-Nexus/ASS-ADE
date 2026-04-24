"""Tier a2 — assimilated class 'NexusTransportMissing'

Assimilated from: nexus.py:83-92
"""

from __future__ import annotations


# --- assimilated symbol ---
class NexusTransportMissing(NexusError):
    """No ``NexusTransport`` was wired into the binder call.

    Distinct from :class:`NexusUnavailable` (transport tried, failed).
    This is a configuration gap: the caller invoked ``bind()`` without
    an ``nexus_transport`` argument. Production callers MUST provide
    one; tests may opt out by passing ``nexus_transport=None``
    explicitly (in which case the binder runs the offline scoring
    path and does NOT pretend to have run Nexus checks).
    """

