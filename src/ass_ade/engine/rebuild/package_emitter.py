"""Package Emitter — turn a rebuild folder into a pip-installable Python package.

Writes ``__init__.py`` per tier (with real imports, not just ``__all__`` lists)
and a root ``pyproject.toml`` that includes the source project's dependencies
and CLI entry points.
"""

from __future__ import annotations

import ast
import re
import sys
from pathlib import Path
from typing import Any

TIER_NAMES: tuple[str, ...] = (
    "a0_qk_constants",
    "a1_at_functions",
    "a2_mo_composites",
    "a3_og_features",
    "a4_sy_orchestration",
)


def _enforce_boundary(path: Path, control_root: Path) -> None:
    try:
        path.resolve().relative_to(control_root.resolve())
    except ValueError:
        raise RuntimeError(
            f"Security boundary: attempted write to {path!r} "
            f"outside rebuild root {control_root!r}."
        )


def _extract_public_names(py_path: Path) -> list[str]:
    """Return top-level public names (functions, classes, assignments) from a .py file."""
    try:
        source = py_path.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(source, filename=str(py_path))
    except SyntaxError:
        return []
    names: list[str] = []
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if not node.name.startswith("_"):
                names.append(node.name)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and not target.id.startswith("_"):
                    names.append(target.id)
    return names


def _build_tier_init(py_files: list[Path]) -> str:
    """Generate a tier __init__.py that actually imports public symbols."""
    lines: list[str] = ['"""Auto-generated tier package."""', ""]
    all_exported: list[str] = []

    for py_file in sorted(py_files):
        stem = py_file.stem
        names = _extract_public_names(py_file)
        if names:
            lines.append(f"from .{stem} import {', '.join(sorted(names))}")
            all_exported.extend(names)
        else:
            lines.append(f"from . import {stem}")

    if all_exported:
        lines.append("")
        lines.append("__all__ = [")
        for name in sorted(set(all_exported)):
            lines.append(f'    "{name}",')
        lines.append("]")

    lines.append("")
    return "\n".join(lines)


def _build_top_init(tier_names: list[str]) -> str:
    """Generate root __init__.py that imports each tier subpackage."""
    lines: list[str] = ['"""Auto-generated rebuild package."""', ""]
    for tier in sorted(tier_names):
        lines.append(f"from . import {tier}")
    if tier_names:
        lines.append("")
        lines.append("__all__ = [")
        for tier in sorted(tier_names):
            lines.append(f'    "{tier}",')
        lines.append("]")
    lines.append("")
    return "\n".join(lines)


def _read_source_pyproject(source_root: Path) -> tuple[list[str], dict[str, str]]:
    """Read dependencies and scripts from the source project's pyproject.toml.

    Walks up the directory tree from ``source_root`` to find the nearest
    ``pyproject.toml`` (handles ``src/`` layout projects).

    Returns (deps_list, scripts_dict).
    """
    # Walk up the directory tree to find pyproject.toml
    candidate = source_root
    pyproject = None
    for _ in range(5):  # limit search depth
        if (candidate / "pyproject.toml").exists():
            pyproject = candidate / "pyproject.toml"
            break
        parent = candidate.parent
        if parent == candidate:
            break
        candidate = parent

    if pyproject is None:
        return [], {}
    text = pyproject.read_text(encoding="utf-8")
    data: dict[str, Any] = {}
    # Use tomllib (stdlib ≥3.11) with fallback to tomli
    try:
        if sys.version_info >= (3, 11):
            import tomllib
            data = tomllib.loads(text)
        else:
            import tomli  # type: ignore[import-untyped]
            data = tomli.loads(text)
    except Exception:  # noqa: BLE001
        return [], {}
    proj = data.get("project", {})
    deps: list[str] = proj.get("dependencies", [])
    scripts: dict[str, str] = proj.get("scripts", {})
    return deps, scripts


def _find_cli_entry_point(tier_names: list[str], target_root: Path) -> dict[str, str]:
    """Detect a Typer ``app`` or ``def main(`` in a4_sy_orchestration and return scripts."""
    sy_dir = target_root / "a4_sy_orchestration"
    if not sy_dir.exists():
        return {}
    for py_file in sorted(sy_dir.glob("*.py")):
        if py_file.name == "__init__.py":
            continue
        try:
            source = py_file.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        # Typer app pattern
        if re.search(r"^app\s*=\s*typer\.Typer", source, re.MULTILINE):
            cmd = py_file.stem.replace("_", "-")
            return {cmd: f"a4_sy_orchestration.{py_file.stem}:app"}
        # Plain main() pattern
        if re.search(r"^def main\(", source, re.MULTILINE):
            cmd = py_file.stem.replace("_", "-")
            return {cmd: f"a4_sy_orchestration.{py_file.stem}:main"}
    return {}


def _build_pyproject(
    package_name: str,
    deps: list[str] | None = None,
    entry_points: dict[str, str] | None = None,
) -> str:
    dep_block = ""
    if deps:
        dep_lines = "".join(f'    "{d}",\n' for d in deps)
        dep_block = f"dependencies = [\n{dep_lines}]\n"

    script_block = ""
    if entry_points:
        script_lines = "".join(f'{k} = "{v}"\n' for k, v in entry_points.items())
        script_block = f"\n[project.scripts]\n{script_lines}"

    return (
        "[build-system]\n"
        'requires = ["hatchling"]\n'
        'build-backend = "hatchling.build"\n'
        "\n"
        "[project]\n"
        f'name = "{package_name}"\n'
        'version = "0.1.0.dev0"\n'
        'description = "Auto-emitted rebuild package"\n'
        'requires-python = ">=3.11"\n'
        f"{dep_block}"
        f"{script_block}"
        "\n"
        "[tool.hatch.build.targets.wheel]\n"
        'packages = ["."]\n'
    )


def _compile_check(text: str, path: str) -> bool:
    try:
        compile(text, path, "exec")
        return True
    except SyntaxError:
        return False


def emit_runnable_package(
    target_root: Path,
    *,
    package_name: str = "ass_ade_rebuild",
    control_root: Path | None = None,
    source_root: Path | None = None,
) -> dict[str, Any]:
    """Turn a rebuild folder into a pip-installable Python package.

    Args:
        target_root:   The rebuild output folder (e.g. ``output/20260418_153000``).
        package_name:  Name for the generated package.
        control_root:  Safety boundary — writes must stay inside this directory.
        source_root:   Original source directory; used to read dependencies and
                       CLI entry points from its ``pyproject.toml``.

    Returns:
        Dict with ``package_root``, ``init_files``, ``pyproject``, ``importable``.
    """
    target_root = Path(target_root).resolve()
    if control_root is None:
        control_root = target_root

    _enforce_boundary(target_root, control_root)

    # Read source project metadata (deps + scripts)
    source_deps: list[str] = []
    source_scripts: dict[str, str] = {}
    if source_root is not None:
        source_deps, source_scripts = _read_source_pyproject(Path(source_root))

    init_files: list[str] = []
    importable: bool = True
    tier_names_present: list[str] = []

    for tier in TIER_NAMES:
        tier_dir = target_root / tier
        if not tier_dir.is_dir():
            continue
        # Include ALL .py files in the tier directory (not just draft-prefixed ones)
        py_files = [
            f
            for f in sorted(tier_dir.iterdir())
            if f.is_file() and f.suffix == ".py" and f.name != "__init__.py"
        ]
        if not py_files:
            continue

        tier_names_present.append(tier)
        tier_init_path = tier_dir / "__init__.py"
        _enforce_boundary(tier_init_path, control_root)
        tier_init_text = _build_tier_init(py_files)
        tier_init_path.write_text(tier_init_text, encoding="utf-8")
        init_files.append(str(tier_init_path))
        if not _compile_check(tier_init_text, str(tier_init_path)):
            importable = False

    top_init_path = target_root / "__init__.py"
    _enforce_boundary(top_init_path, control_root)
    top_init_text = _build_top_init(tier_names_present)
    top_init_path.write_text(top_init_text, encoding="utf-8")
    init_files.append(str(top_init_path))
    if not _compile_check(top_init_text, str(top_init_path)):
        importable = False

    # Determine CLI entry points: prefer source scripts, fall back to detection
    entry_points = source_scripts or _find_cli_entry_point(tier_names_present, target_root)

    pyproject_path = target_root / "pyproject.toml"
    _enforce_boundary(pyproject_path, control_root)
    pyproject_path.write_text(
        _build_pyproject(package_name, deps=source_deps or None, entry_points=entry_points or None),
        encoding="utf-8",
    )

    return {
        "package_root": str(target_root),
        "init_files": init_files,
        "pyproject": str(pyproject_path),
        "importable": importable,
    }
