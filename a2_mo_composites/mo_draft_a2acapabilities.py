# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_a2acapabilities.py:7
# Component id: mo.source.a2_mo_composites.a2acapabilities
from __future__ import annotations

__version__ = "0.1.0"

class A2ACapabilities(BaseModel):
    """Agent capability flags per A2A spec."""

    streaming: bool = False
    pushNotifications: bool = False
    stateTransitionHistory: bool = False
