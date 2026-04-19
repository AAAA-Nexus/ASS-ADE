# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:78
# Component id: mo.source.a2_mo_composites.get_health
from __future__ import annotations

__version__ = "0.1.0"

def get_health(self) -> HealthStatus:
    """/health — free"""
    return self._get_model("/health", HealthStatus)
