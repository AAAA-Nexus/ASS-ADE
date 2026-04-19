# Extracted from C:/!ass-ade/src/ass_ade/nexus/client.py:273
# Component id: mo.source.ass_ade.get_health
from __future__ import annotations

__version__ = "0.1.0"

def get_health(self) -> HealthStatus:
    """/health — free"""
    return self._get_model("/health", HealthStatus)
