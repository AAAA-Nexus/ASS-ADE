# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_parse_metrics.py:7
# Component id: at.source.a1_at_functions.parse_metrics
from __future__ import annotations

__version__ = "0.1.0"

def parse_metrics(items: Iterable[str]) -> dict[str, Any]:
    metrics: dict[str, Any] = {}
    for item in items:
        for part in item.split(","):
            if not part.strip():
                continue
            if "=" not in part:
                raise ValueError(f"Metric must use key=value format: {part}")
            key, value = part.split("=", 1)
            key = key.strip()
            if not key:
                raise ValueError("Metric key cannot be empty")
            metrics[key] = _coerce_metric_value(value)
    return metrics
