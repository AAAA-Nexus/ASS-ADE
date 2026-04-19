# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_preview.py:7
# Component id: at.source.a1_at_functions.preview
from __future__ import annotations

__version__ = "0.1.0"

def preview(self, plan: EditPlan) -> str:
    """Return a combined diff of all edits in the plan."""
    if not plan.validated:
        errs = self.validate(plan)
        if errs:
            return "Validation errors:\n" + "\n".join(f"  ✗ {e}" for e in errs)
    return "\n\n".join(
        f"--- {e.description} ---\n{e.diff}" for e in plan.edits if e.diff
    )
