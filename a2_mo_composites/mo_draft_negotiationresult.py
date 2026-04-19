# Extracted from C:/!ass-ade/src/ass_ade/a2a/__init__.py:250
# Component id: mo.source.ass_ade.negotiationresult
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
