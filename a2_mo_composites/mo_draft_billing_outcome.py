# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:986
# Component id: mo.source.a2_mo_composites.billing_outcome
from __future__ import annotations

__version__ = "0.1.0"

def billing_outcome(self, task_id: str, success: bool, metric_value: float, **kwargs: Any) -> BillingOutcome:
    """/v1/billing/outcome — pay only for measurably successful tasks (PAY-509). $0.040/call"""
    return self._post_model("/v1/billing/outcome", BillingOutcome, {
        "task_id": task_id, "success": success, "metric_value": metric_value, **kwargs,
    })
