# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:992
# Component id: mo.source.a2_mo_composites.costs_attribute
from __future__ import annotations

__version__ = "0.1.0"

def costs_attribute(self, run_id: str, **kwargs: Any) -> CostAttribution:
    """/v1/costs/attribute — token spend by agent/task/model (DEV-603). $0.040/call"""
    return self._post_model("/v1/costs/attribute", CostAttribution, {"run_id": run_id, **kwargs})
