# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testeditplanexecutor.py:7
# Component id: mo.source.a2_mo_composites.testeditplanexecutor
from __future__ import annotations

__version__ = "0.1.0"

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
