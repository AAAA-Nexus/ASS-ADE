# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a0_qk_constants/qk_draft_update_from_usage.py:7
# Component id: qk.source.a0_qk_constants.update_from_usage
from __future__ import annotations

__version__ = "0.1.0"

def update_from_usage(self, usage: dict[str, int] | None) -> None:
    """Update running totals from a completion response's usage dict."""
    if not usage:
        return
    self.prompt_tokens = usage.get("prompt_tokens", self.prompt_tokens)
    self.completion_tokens += usage.get("completion_tokens", 0)
    self.total_calls += 1
