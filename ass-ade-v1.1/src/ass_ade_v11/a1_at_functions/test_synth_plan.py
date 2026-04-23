"""Pure plan for import-smoke coverage over ``src/ass_ade_v11`` (MAP=TERRAIN)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def qualname_for_src_py(py_file: Path, repo_root: Path) -> str:
    """Map ``src/ass_ade_v11/.../*.py`` to dotted import name."""
    rel = py_file.relative_to(repo_root / "src").with_suffix("")
    parts = list(rel.parts)
    if parts[-1] == "__init__":
        parts = parts[:-1]
    return ".".join(parts)


def iter_src_py_files(repo_root: Path) -> list[Path]:
    root = repo_root / "src" / "ass_ade_v11"
    return sorted(root.rglob("*.py"))


def list_expected_qualnames(repo_root: Path) -> list[str]:
    """Sorted unique import paths for every Python file under ``ass_ade_v11``."""
    seen: set[str] = set()
    for f in iter_src_py_files(repo_root):
        seen.add(qualname_for_src_py(f, repo_root))
    return sorted(seen)


def load_manifest_qualnames(repo_root: Path) -> list[str] | None:
    path = repo_root / "tests" / "generated_smoke" / "_qualnames.json"
    if not path.is_file():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("manifest must be a JSON list of strings")
    return [str(x) for x in data]


def manifest_drift(repo_root: Path) -> dict[str, Any]:
    """Compare on-disk manifest to expected qualnames."""
    expected = list_expected_qualnames(repo_root)
    current = load_manifest_qualnames(repo_root)
    if current is None:
        return {"ok": False, "reason": "missing_file", "expected": expected, "current": None}
    if current != expected:
        return {"ok": False, "reason": "drift", "expected": expected, "current": current}
    return {"ok": True, "expected": expected, "current": current}


def plan_manifest_payload(repo_root: Path) -> str:
    """Stable JSON text for ``_qualnames.json``."""
    names = list_expected_qualnames(repo_root)
    return json.dumps(names, indent=2, ensure_ascii=True) + "\n"
