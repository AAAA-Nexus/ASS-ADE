# Extracted from C:/!ass-ade/src/ass_ade/protocol/evolution.py:178
# Component id: at.source.ass_ade.parse_metrics
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
