# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_editplanexecutor.py:5
# Component id: mo.source.ass_ade.editplanexecutor
__version__ = "0.1.0"

class EditPlanExecutor:
    """Validates and atomically applies edit plans.

    Uses FileHistory for snapshots so every applied plan can be undone.
    """

    def __init__(self, working_dir: str = ".", history: FileHistory | None = None) -> None:
        self._cwd = Path(working_dir).resolve()
        self._history = history or FileHistory(working_dir)

    def validate(self, plan: EditPlan) -> list[str]:
        """Validate a plan, populating diffs and detecting conflicts.

        Returns a list of error messages (empty = valid).
        """
        errors: list[str] = []

        for edit in plan.edits:
            target = self._cwd / edit.path

            if edit.kind == EditKind.CREATE:
                if target.exists():
                    errors.append(f"CREATE conflict: {edit.path} already exists.")
                edit.diff = _create_diff(edit.path, edit.new_string)

            elif edit.kind == EditKind.MODIFY:
                if not target.is_file():
                    errors.append(f"MODIFY target not found: {edit.path}")
                    continue
                text = target.read_text(encoding="utf-8")
                count = text.count(edit.old_string)
                if count == 0:
                    errors.append(
                        f"MODIFY: old_string not found in {edit.path}"
                    )
                elif count > 1:
                    errors.append(
                        f"MODIFY: old_string matches {count} locations in {edit.path}"
                    )
                else:
                    new_text = text.replace(edit.old_string, edit.new_string, 1)
                    edit.diff = _modify_diff(edit.path, text, new_text)
                    edit._original_content = text

            elif edit.kind == EditKind.DELETE:
                if not target.exists():
                    errors.append(f"DELETE target not found: {edit.path}")
                elif target.is_file():
                    edit._original_content = target.read_text(encoding="utf-8")

        if not errors:
            plan.validated = True
        return errors

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

    def preview(self, plan: EditPlan) -> str:
        """Return a combined diff of all edits in the plan."""
        if not plan.validated:
            errs = self.validate(plan)
            if errs:
                return "Validation errors:\n" + "\n".join(f"  ✗ {e}" for e in errs)
        return "\n\n".join(
            f"--- {e.description} ---\n{e.diff}" for e in plan.edits if e.diff
        )
