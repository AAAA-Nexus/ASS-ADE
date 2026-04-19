"""Multi-file atomic edit plans.

An EditPlan is a sequence of file operations that are:
  1. Proposed — the agent describes what it wants to change.
  2. Validated — diffs are generated, conflicts detected.
  3. Applied atomically — all edits succeed or none do (rollback on failure).

This gives ASS-ADE a "plan → review → apply" workflow that is safer than
streaming edits one-at-a-time. Every file is snapshotted before mutation
via FileHistory, so the entire plan can be reverted.

Formal invariant (atomicity):
    Let P = {e₁, e₂, ..., eₙ} be an edit plan.
    Either ∀eᵢ ∈ P: applied(eᵢ) = true,
    or     ∀eᵢ ∈ P: applied(eᵢ) = false ∧ file(eᵢ) = original(eᵢ).
"""

from __future__ import annotations

import difflib
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

from ass_ade.tools.base import ToolResult
from ass_ade.tools.history import FileHistory


class EditKind(str, Enum):
    CREATE = "create"
    MODIFY = "modify"
    DELETE = "delete"


@dataclass
class PlannedEdit:
    """A single file operation within an edit plan."""

    kind: EditKind
    path: str  # relative to working dir
    old_string: str = ""  # for MODIFY
    new_string: str = ""  # for MODIFY and CREATE
    description: str = ""
    diff: str = ""  # populated during validation

    # Internal state
    _original_content: str | None = None


@dataclass
class EditPlan:
    """A batch of file operations to apply atomically."""

    edits: list[PlannedEdit] = field(default_factory=list)
    description: str = ""
    validated: bool = False
    applied: bool = False

    def add_create(self, path: str, content: str, description: str = "") -> None:
        self.edits.append(PlannedEdit(
            kind=EditKind.CREATE,
            path=path,
            new_string=content,
            description=description or f"Create {path}",
        ))
        self.validated = False

    def add_modify(
        self, path: str, old_string: str, new_string: str, description: str = ""
    ) -> None:
        self.edits.append(PlannedEdit(
            kind=EditKind.MODIFY,
            path=path,
            old_string=old_string,
            new_string=new_string,
            description=description or f"Edit {path}",
        ))
        self.validated = False

    def add_delete(self, path: str, description: str = "") -> None:
        self.edits.append(PlannedEdit(
            kind=EditKind.DELETE,
            path=path,
            description=description or f"Delete {path}",
        ))
        self.validated = False


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


def _create_diff(path: str, content: str) -> str:
    return "".join(difflib.unified_diff(
        [],
        content.splitlines(keepends=True),
        fromfile="/dev/null",
        tofile=f"b/{path}",
    ))


def _modify_diff(path: str, old_text: str, new_text: str) -> str:
    return "".join(difflib.unified_diff(
        old_text.splitlines(keepends=True),
        new_text.splitlines(keepends=True),
        fromfile=f"a/{path}",
        tofile=f"b/{path}",
    ))
