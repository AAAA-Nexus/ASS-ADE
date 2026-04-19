# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_engineorchestrator.py:219
# Component id: mo.source.a2_mo_composites.check_conviction_gate
from __future__ import annotations

__version__ = "0.1.0"

def check_conviction_gate(self, tool_name: str, args: dict) -> bool:
    """Return True if the tool call should be BLOCKED due to low conviction.

    Only blocks destructive tools when conviction is below threshold.
    Fail-open: returns False (don't block) on any error.
    """
    if tool_name not in self._destructive_tools:
        return False
    try:
        conviction = self.wisdom.conviction if self._wisdom else 0.5
        if conviction < self._conviction_threshold and self.wisdom._audits > 0:
            _LOG.warning(
                "Conviction gate: %s blocked (conviction=%.2f < %.2f)",
                tool_name, conviction, self._conviction_threshold,
            )
            return True
    except Exception as exc:
        _LOG.debug("conviction gate check failed (fail-open): %s", exc)
    return False
