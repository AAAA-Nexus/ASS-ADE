"""Tests for Cap-B finish pipeline (stub detection + in-place completion)."""

from __future__ import annotations

from pathlib import Path

import pytest

from ass_ade.engine.rebuild import finish as F
from ass_ade.engine.rebuild.finish import (
    _apply_body,
    finish_project,
    scan_path,
)


SAMPLE = '''"""Sample module."""


def ready(x: int) -> int:
    return x + 1


def todo_me(x: int) -> int:
    """Add 2 to x."""
    pass


def not_yet(x: int) -> int:
    raise NotImplementedError


class Widget:
    def ellipsis_method(self) -> None:
        ...
'''


def _write(tmp_path: Path, name: str = "sample.py") -> Path:
    p = tmp_path / name
    p.write_text(SAMPLE, encoding="utf-8")
    return p


def test_scan_detects_only_incomplete(tmp_path: Path) -> None:
    _write(tmp_path)
    found = scan_path(tmp_path)
    qualnames = {f.qualname for f in found}
    assert "todo_me" in qualnames
    assert "not_yet" in qualnames
    assert "Widget.ellipsis_method" in qualnames
    assert "ready" not in qualnames


def test_scan_ignores_venv_and_cache(tmp_path: Path) -> None:
    (tmp_path / ".venv").mkdir()
    (tmp_path / ".venv" / "evil.py").write_text("def bad():\n    pass\n", encoding="utf-8")
    (tmp_path / "__pycache__").mkdir()
    (tmp_path / "__pycache__" / "cached.py").write_text("def bad():\n    pass\n", encoding="utf-8")
    _write(tmp_path)
    found = scan_path(tmp_path)
    assert all(".venv" not in f.path.parts and "__pycache__" not in f.path.parts for f in found)


def test_apply_body_replaces_correctly(tmp_path: Path) -> None:
    path = _write(tmp_path)
    fns = [f for f in scan_path(tmp_path) if f.qualname == "todo_me"]
    assert fns
    fn = fns[0]
    source = path.read_text(encoding="utf-8")
    updated = _apply_body(source, fn, 'return x + 2')
    assert "return x + 2" in updated
    assert "pass" not in updated.split("def todo_me")[1].split("def ")[0]


def test_finish_project_rejects_when_nexus_unreachable(tmp_path: Path, monkeypatch) -> None:
    _write(tmp_path)
    monkeypatch.setattr(F, "_synthesize_via_nexus", lambda **kw: None)
    receipt = finish_project(
        tmp_path,
        api_key="dummy",
        max_refinement_attempts=1,
    )
    assert receipt["completed_count"] == 0
    assert receipt["rejected_count"] >= 3  # three stubs in SAMPLE
    assert all(r["reason"] == "refinement_exhausted" for r in receipt["rejected"])


def test_finish_project_applies_successful_completion(tmp_path: Path, monkeypatch) -> None:
    path = _write(tmp_path)

    def fake_synth(**kwargs):
        name = kwargs["component_id"].split(".")[-1]
        return f"def {name}(*args, **kwargs):\n    return 42\n"

    monkeypatch.setattr(F, "_synthesize_via_nexus", fake_synth)
    receipt = finish_project(
        tmp_path,
        api_key="dummy",
        apply_in_place=True,
        max_refinement_attempts=1,
    )
    assert receipt["completed_count"] >= 3
    new_source = path.read_text(encoding="utf-8")
    assert "return 42" in new_source
    # Original healthy function preserved.
    assert "return x + 1" in new_source


def test_finish_project_writes_patches_without_apply(tmp_path: Path, monkeypatch) -> None:
    path = _write(tmp_path)

    def fake_synth(**kwargs):
        return "return 0"

    monkeypatch.setattr(F, "_synthesize_via_nexus", fake_synth)
    finish_project(
        tmp_path,
        api_key="dummy",
        apply_in_place=False,
        max_refinement_attempts=1,
    )
    # Source unchanged.
    assert path.read_text(encoding="utf-8") == SAMPLE
    # Patched file written.
    patched = tmp_path / ".ass-ade" / "patches" / "sample.py.patched"
    assert patched.exists()
    assert "return 0" in patched.read_text(encoding="utf-8")
    receipt = tmp_path / ".ass-ade" / "patches" / "finish_receipt.json"
    assert receipt.exists()
