"""Tests for tools.plan — multi-file atomic edit plans."""

from __future__ import annotations

from pathlib import Path

import pytest

from ass_ade.tools.history import FileHistory
from ass_ade.tools.plan import EditKind, EditPlan, EditPlanExecutor


@pytest.fixture
def workspace(tmp_path: Path) -> Path:
    (tmp_path / "main.py").write_text("def main():\n    pass\n", encoding="utf-8")
    (tmp_path / "utils.py").write_text("def helper():\n    return 42\n", encoding="utf-8")
    return tmp_path


@pytest.fixture
def executor(workspace: Path) -> EditPlanExecutor:
    history = FileHistory(str(workspace))
    return EditPlanExecutor(str(workspace), history=history)


class TestEditPlan:
    def test_add_create(self):
        plan = EditPlan(description="Test plan")
        plan.add_create("new.py", "print('new')\n")
        assert len(plan.edits) == 1
        assert plan.edits[0].kind == EditKind.CREATE

    def test_add_modify(self):
        plan = EditPlan()
        plan.add_modify("main.py", "pass", "print('hello')")
        assert len(plan.edits) == 1
        assert plan.edits[0].kind == EditKind.MODIFY

    def test_add_delete(self):
        plan = EditPlan()
        plan.add_delete("old.py")
        assert len(plan.edits) == 1
        assert plan.edits[0].kind == EditKind.DELETE

    def test_adding_resets_validated(self):
        plan = EditPlan()
        plan.validated = True
        plan.add_create("x.py", "x")
        assert plan.validated is False


class TestEditPlanExecutor:
    def test_validate_create_success(self, executor: EditPlanExecutor):
        plan = EditPlan()
        plan.add_create("brand_new.py", "content")
        errors = executor.validate(plan)
        assert errors == []
        assert plan.validated is True

    def test_validate_create_conflict(self, executor: EditPlanExecutor):
        plan = EditPlan()
        plan.add_create("main.py", "conflict")
        errors = executor.validate(plan)
        assert len(errors) == 1
        assert "already exists" in errors[0]

    def test_validate_modify_success(self, executor: EditPlanExecutor):
        plan = EditPlan()
        plan.add_modify("main.py", "pass", "print('hello')")
        errors = executor.validate(plan)
        assert errors == []
        assert plan.validated is True
        assert plan.edits[0].diff  # diff populated

    def test_validate_modify_not_found(self, executor: EditPlanExecutor):
        plan = EditPlan()
        plan.add_modify("main.py", "NONEXISTENT", "replacement")
        errors = executor.validate(plan)
        assert len(errors) == 1
        assert "not found" in errors[0]

    def test_validate_modify_file_missing(self, executor: EditPlanExecutor):
        plan = EditPlan()
        plan.add_modify("ghost.py", "old", "new")
        errors = executor.validate(plan)
        assert len(errors) == 1

    def test_validate_delete_success(self, executor: EditPlanExecutor):
        plan = EditPlan()
        plan.add_delete("main.py")
        errors = executor.validate(plan)
        assert errors == []

    def test_validate_delete_not_found(self, executor: EditPlanExecutor):
        plan = EditPlan()
        plan.add_delete("nonexistent.py")
        errors = executor.validate(plan)
        assert len(errors) == 1

    def test_apply_create(self, executor: EditPlanExecutor, workspace: Path):
        plan = EditPlan()
        plan.add_create("created.py", "print('created')\n")
        executor.validate(plan)
        result = executor.apply(plan)
        assert result.success
        assert (workspace / "created.py").read_text(encoding="utf-8") == "print('created')\n"
        assert plan.applied is True

    def test_apply_modify(self, executor: EditPlanExecutor, workspace: Path):
        plan = EditPlan()
        plan.add_modify("main.py", "pass", "print('hello')")
        executor.validate(plan)
        result = executor.apply(plan)
        assert result.success
        content = (workspace / "main.py").read_text(encoding="utf-8")
        assert "print('hello')" in content

    def test_apply_delete(self, executor: EditPlanExecutor, workspace: Path):
        plan = EditPlan()
        plan.add_delete("utils.py")
        executor.validate(plan)
        result = executor.apply(plan)
        assert result.success
        assert not (workspace / "utils.py").exists()

    def test_apply_unvalidated_fails(self, executor: EditPlanExecutor):
        plan = EditPlan()
        plan.add_create("x.py", "x")
        result = executor.apply(plan)
        assert not result.success
        assert "validated" in result.error.lower()

    def test_apply_multi_file(self, executor: EditPlanExecutor, workspace: Path):
        plan = EditPlan(description="Multi-file edit")
        plan.add_modify("main.py", "pass", "print('main')")
        plan.add_modify("utils.py", "return 42", "return 99")
        plan.add_create("new.py", "# new file\n")
        executor.validate(plan)
        result = executor.apply(plan)
        assert result.success
        assert "print('main')" in (workspace / "main.py").read_text(encoding="utf-8")
        assert "return 99" in (workspace / "utils.py").read_text(encoding="utf-8")
        assert (workspace / "new.py").exists()

    def test_preview(self, executor: EditPlanExecutor):
        plan = EditPlan()
        plan.add_modify("main.py", "pass", "print('hello')")
        preview = executor.preview(plan)
        assert "pass" in preview or "print" in preview

    def test_preview_with_validation_errors(self, executor: EditPlanExecutor):
        plan = EditPlan()
        plan.add_modify("ghost.py", "old", "new")
        preview = executor.preview(plan)
        assert "error" in preview.lower() or "Validation" in preview
