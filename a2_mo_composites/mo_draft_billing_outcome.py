# Extracted from C:/!ass-ade/src/ass_ade/nexus/client.py:1181
# Component id: mo.source.ass_ade.billing_outcome
from __future__ import annotations

__version__ = "0.1.0"

def billing_outcome(self, task_id: str, success: bool, metric_value: float, **kwargs: Any) -> BillingOutcome:
    """/v1/billing/outcome — pay only for measurably successful tasks (PAY-509). $0.040/call"""
    return self._post_model("/v1/billing/outcome", BillingOutcome, {
        "task_id": task_id, "success": success, "metric_value": metric_value, **kwargs,
    })
