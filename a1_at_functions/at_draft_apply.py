# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_apply.py:7
# Component id: at.source.a1_at_functions.apply
from __future__ import annotations

__version__ = "0.1.0"

def apply(self, plan: EditPlan) -> ToolResult:
    """Apply a validated plan atomically.

    If any edit fails, all previously applied edits in this plan
    are rolled back via FileHistory.
    """
    if not plan.validated:
        return ToolResult(error="Plan must be validated before applying.", success=False)

    applied_paths: list[str] = []

    try:
        for edit in plan.edits:
            target = self._cwd / edit.path

            if edit.kind == EditKind.CREATE:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(edit.new_string, encoding="utf-8")
                applied_paths.append(edit.path)

            elif edit.kind == EditKind.MODIFY:
                # Snapshot before mutation
                if edit._original_content is not None:
                    self._history.record(edit.path, edit._original_content)
                text = target.read_text(encoding="utf-8")
                new_text = text.replace(edit.old_string, edit.new_string, 1)
                target.write_text(new_text, encoding="utf-8")
                applied_paths.append(edit.path)

            elif edit.kind == EditKind.DELETE:
                if edit._original_content is not None:
                    self._history.record(edit.path, edit._original_content)
                target.unlink()
                applied_paths.append(edit.path)

    except Exception as exc:
        # ── Rollback ──────────────────────────────────────────────────
        for rpath in reversed(applied_paths):
            try:
                self._history.undo(rpath)
            except Exception:
                pass  # Best-effort rollback
        plan.applied = False
        return ToolResult(
            error=f"Plan failed at {edit.path}: {exc}. Rolled back {len(applied_paths)} edits.",
            success=False,
        )

    plan.applied = True
    summary = "\n".join(f"  ✓ {e.description}" for e in plan.edits)
    return ToolResult(output=f"Applied {len(plan.edits)} edits:\n{summary}")
