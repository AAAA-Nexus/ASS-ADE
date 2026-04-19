# Extracted from C:/!ass-ade/src/ass_ade/a2a/__init__.py:71
# Component id: mo.source.ass_ade.a2acapabilities
from __future__ import annotations

__version__ = "0.1.0"

class A2ACapabilities(BaseModel):
    """Agent capability flags per A2A spec."""

    streaming: bool = False
    pushNotifications: bool = False
    stateTransitionHistory: bool = False
