# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_on_tool_event.py:7
# Component id: at.source.a1_at_functions.on_tool_event
from __future__ import annotations

__version__ = "0.1.0"

def on_tool_event(self, tool_name: str, args: dict, result_content: str) -> list:
    """Called after each tool execution. Returns list of BAS alerts fired."""
    self._step_tool_counts[tool_name] = self._step_tool_counts.get(tool_name, 0) + 1
    self._step_tool_results.append(f"{tool_name}:{result_content[:50]}")

    alerts = []
    try:
        max_repeat = max(self._step_tool_counts.values()) if self._step_tool_counts else 0
        metrics = {
            "tool_repeat_count": max_repeat,
            "synergy": 0.0,
            "novelty": 0.0,
            "gvu_delta": 0.0,
        }
        new_alerts = self.bas.monitor_all(metrics)
        alerts.extend(new_alerts)
    except Exception as exc:
        _LOG.debug("bas.on_tool_event failed: %s", exc)

    return alerts
