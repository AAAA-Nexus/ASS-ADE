"""Pure plan for import-smoke coverage over ``src/ass_ade`` (MAP=TERRAIN)."""

from __future__ import annotations

import json
import textwrap
from pathlib import Path
from typing import Any


def _qualname_for_package_py(py_file: Path, package_root: Path, package_name: str) -> str:
    rel = py_file.relative_to(package_root).with_suffix("")
    parts = list(rel.parts)
    parts.insert(0, package_name)
    if parts[-1] == "__init__":
        parts = parts[:-1]
    return ".".join(parts)


def qualname_for_src_py(py_file: Path, repo_root: Path) -> str:
    """Map ``src/ass_ade/.../*.py`` to dotted import name."""
    return _qualname_for_package_py(py_file, repo_root / "src" / "ass_ade", "ass_ade")


def _is_vendor_cursor_hook_py(path: Path, ass_pkg: Path) -> bool:
    """True for template hooks shipped for ``materialize`` (not product imports)."""
    vendor = ass_pkg / "ade" / "cursor_hooks_bundled"
    try:
        path.relative_to(vendor)
        return True
    except ValueError:
        return False


def iter_src_py_files(repo_root: Path) -> list[Path]:
    root = repo_root / "src" / "ass_ade"
    return sorted(
        f for f in root.rglob("*.py") if not _is_vendor_cursor_hook_py(f, root)
    )


def list_expected_qualnames(repo_root: Path) -> list[str]:
    """Sorted unique import paths for every Python file under ``ass_ade``."""
    seen: set[str] = set()
    for f in iter_src_py_files(repo_root):
        seen.add(qualname_for_src_py(f, repo_root))
    return sorted(seen)


def list_expected_qualnames_for_package(package_root: Path, package_name: str) -> list[str]:
    """Sorted unique import paths for every Python file under one emitted package root."""
    seen: set[str] = set()
    for f in sorted(package_root.rglob("*.py")):
        if f.name == "__pycache__":
            continue
        seen.add(_qualname_for_package_py(f, package_root, package_name))
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


def plan_manifest_payload_for_package(package_root: Path, package_name: str) -> str:
    names = list_expected_qualnames_for_package(package_root, package_name)
    return json.dumps(names, indent=2, ensure_ascii=True) + "\n"


def generated_smoke_test_source() -> str:
    """Stable pytest smoke test used by emitted package layouts."""
    return textwrap.dedent(
        '''\
        """Import smoke tests — manifest driven (regenerate via ``ass-ade book synth-tests``)."""

        from __future__ import annotations

        import importlib
        import json
        from pathlib import Path

        import pytest

        _MAN = Path(__file__).resolve().parent / "_qualnames.json"
        QUALNAMES: list[str] = json.loads(_MAN.read_text(encoding="utf-8"))


        @pytest.mark.generated_smoke
        @pytest.mark.parametrize("qualname", QUALNAMES)
        def test_import_smoke(qualname: str) -> None:
            mod = importlib.import_module(qualname)
            assert mod is not None
        '''
    )
