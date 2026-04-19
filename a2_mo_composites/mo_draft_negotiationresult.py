# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_negotiationresult.py:7
# Component id: mo.source.a2_mo_composites.negotiationresult
from __future__ import annotations

__version__ = "0.1.0"

class NegotiationResult:
    """Result of comparing two agent cards for interop."""

    compatible: bool
    shared_skills: list[str] = field(default_factory=list)
    local_only: list[str] = field(default_factory=list)
    remote_only: list[str] = field(default_factory=list)
    auth_compatible: bool = True
    notes: list[str] = field(default_factory=list)
